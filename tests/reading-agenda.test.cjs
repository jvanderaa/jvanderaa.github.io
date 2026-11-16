const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const { test } = require('node:test');

const source = fs.readFileSync(`${__dirname}/../assets/js/reading-agenda.js`, 'utf8');

// A minimal element model: enough DOM for the agenda script, nothing more.
function el(tag, init = {}) {
  const node = {
    nodeType: 1,
    tagName: tag.toUpperCase(),
    parentElement: null,
    childNodes: [],
    children: [],
    attrs: {},
    classes: new Set(),
    listeners: {},
    dataset: {},
    hidden: false,
    style: { props: {}, setProperty(name, value) { this.props[name] = value; } },
    ...init,
  };
  node.classList = {
    add: (name) => node.classes.add(name),
    remove: (name) => node.classes.delete(name),
    contains: (name) => node.classes.has(name),
    toggle: (name, force) => {
      const on = force === undefined ? !node.classes.has(name) : force;
      if (on) node.classes.add(name);
      else node.classes.delete(name);
      return on;
    },
  };
  node.setAttribute = (name, value) => { node.attrs[name] = value; };
  node.removeAttribute = (name) => { delete node.attrs[name]; };
  node.getAttribute = (name) => node.attrs[name];
  node.appendChild = (child) => {
    node.childNodes.push(child);
    if (child.nodeType === 1) {
      node.children.push(child);
      child.parentElement = node;
    }
    return child;
  };
  node.contains = (other) => {
    for (let current = other; current; current = current.parentElement) {
      if (current === node) return true;
    }
    return false;
  };
  node.addEventListener = (name, callback) => { node.listeners[name] = callback; };
  Object.defineProperty(node, 'textContent', {
    get: () => node.childNodes.map((child) => child.textContent).join(''),
    set: (value) => { node.childNodes = [text(value)]; node.children = []; },
  });
  return node;
}

function text(value) {
  return { nodeType: 3, textContent: value };
}

function paragraph(count) {
  const p = el('p');
  p.appendChild(text(Array.from({ length: count }, () => 'word').join(' ')));
  return p;
}

function item(link) {
  const li = el('li');
  li.appendChild(link);
  return li;
}

// Hugo with startLevel = 1: <ul><li><ul><li>h2</li><li>h2<ul><li>h3</li></ul></li><li>h2</li></ul></li></ul>
const LABELS = ['Start here', 'Build the lab', 'Work out the address', 'Wrap up'];
const DEPTHS = [0, 0, 1, 0];

function fixture({ isDesktop = true, withBar = false, orphan = false } = {}) {
  const windowEvents = {};
  const documentEvents = {};
  const state = {
    positions: [400, 800, 1000, 1200],
    hidden: [false, false, false, false],
    top: 100,
    bottom: 1600,
    agendaBottom: 300,
  };

  const content = el('div', { getBoundingClientRect: () => ({ top: state.top, bottom: state.bottom }) });
  const links = LABELS.map((label, index) => {
    const link = el('a', { hash: `#section-${index}` });
    link.appendChild(text(label));
    return link;
  });
  const orphanLink = el('a', { hash: '#missing' });
  orphanLink.appendChild(text('Removed section'));
  const headings = links.map((_, index) => el('h2', {
    getBoundingClientRect: () => ({ top: state.hidden[index] ? 0 : state.positions[index] }),
    getClientRects: () => (state.hidden[index] ? [] : [{}]),
    closest: () => content,
  }));

  // Intro 50 words; sections of 213, 213 (+ a collapsed admonition), 213 and 213 words.
  const details = el('details', { open: false });
  const summary = el('summary');
  summary.appendChild(text('Example output'));
  details.appendChild(summary);
  details.appendChild(paragraph(500));
  const labBody = el('div');
  labBody.appendChild(paragraph(213));
  labBody.appendChild(details);
  // The h3 sits inside a shortcode wrapper, not directly in the content element.
  const wrapper = el('div');
  wrapper.appendChild(headings[2]);
  wrapper.appendChild(paragraph(213));
  [paragraph(50), headings[0], paragraph(213), headings[1], labBody, wrapper, headings[3], paragraph(213)]
    .forEach((block) => content.appendChild(block));

  const agenda = el('details', { open: true });
  const nav = el('nav');
  const outer = el('ul');
  const wrapItem = el('li');
  const inner = el('ul');
  const nested = el('ul');
  agenda.appendChild(nav);
  nav.appendChild(outer);
  outer.appendChild(wrapItem);
  wrapItem.appendChild(inner);
  inner.appendChild(item(links[0]));
  const labItem = item(links[1]);
  inner.appendChild(labItem);
  labItem.appendChild(nested);
  nested.appendChild(item(links[2]));
  inner.appendChild(item(links[3]));
  if (orphan) inner.appendChild(item(orphanLink));
  const allLinks = orphan ? links.concat(orphanLink) : links;

  const progress = el('span', { hidden: true });
  const meter = el('div', { hidden: true });
  outer.querySelectorAll = () => allLinks;
  outer.cloneNode = () => {
    const copies = allLinks.map((link) => {
      const copy = el('a', { hash: link.hash, attrs: { ...link.attrs } });
      copy.appendChild(text(link.textContent));
      return copy;
    });
    return el('ul', { querySelectorAll: () => copies, copies });
  };
  Object.assign(agenda, {
    querySelectorAll: () => allLinks,
    querySelector: (selector) => ({
      '[data-agenda-progress]': progress,
      '[data-agenda-meter]': meter,
      'nav > ul': outer,
    })[selector] || null,
    closest: () => null,
    getBoundingClientRect: () => ({ bottom: state.agendaBottom }),
  });
  agenda.addEventListener = (name, callback) => { windowEvents[`agenda:${name}`] = callback; };

  let bar = null;
  let backdrop = null;
  if (withBar) {
    const parts = {
      toggle: el('button', { focused: false }),
      panel: el('div', { hidden: true, querySelectorAll: () => [] }),
      links: el('nav'),
      meta: el('span'),
      title: el('span'),
      fill: el('span'),
    };
    parts.toggle.focus = (options) => { parts.toggle.focused = true; parts.toggle.focusOptions = options; };
    parts.links.querySelector = () => null;
    bar = el('div', {
      hidden: true,
      dataset: { title: 'Example post' },
      parts,
      querySelector: (selector) => ({
        '[data-bar-toggle]': parts.toggle,
        '[data-bar-panel]': parts.panel,
        '[data-bar-links]': parts.links,
        '[data-bar-meta]': parts.meta,
        '[data-bar-title]': parts.title,
        '[data-bar-fill]': parts.fill,
      })[selector] || null,
    });
    backdrop = el('div', { hidden: true });
  }

  const media = { matches: isDesktop, addEventListener() {} };
  const window = {
    innerHeight: 900,
    scrollY: 0,
    matchMedia: () => media,
    requestAnimationFrame: (callback) => callback(),
    addEventListener: (name, callback) => { windowEvents[name] = callback; },
  };
  const document = {
    querySelector: (selector) => ({
      '[data-reading-agenda]': agenda,
      '[data-reading-bar]': bar,
      '[data-bar-backdrop]': backdrop,
    })[selector] || null,
    getElementById: (id) => (/^section-\d+$/.test(id) ? headings[Number(id.slice(8))] : null),
    createElement: (tag) => el(tag),
    addEventListener: (name, callback) => { documentEvents[name] = callback; },
    body: el('body'),
    documentElement: { scrollHeight: 10000 },
    activeElement: null,
  };
  vm.runInNewContext(source, { window, document });
  return {
    state, links, orphanLink, progress, meter, bar, backdrop, media, window, document,
    events: windowEvents, documentEvents,
  };
}

function timeLabel(link) {
  return link.children.find((child) => child.className === 'agenda-time').textContent;
}

function spokenLabel(link) {
  return link.children.find((child) => child.className === 'agenda-sr').textContent;
}

function scrollTo(f, positions, extra = {}) {
  f.state.positions = positions;
  Object.assign(f.state, extra);
  f.events.scroll();
}

test('the introduction leaves every section upcoming and shows the total reading time', () => {
  const { links, progress, meter } = fixture();
  // 902 words, about 3 read: 4 minutes.
  assert.equal(progress.textContent, '4 min read');
  assert.equal(meter.attrs['aria-valuenow'], '0');
  assert.ok(links.every((link) => !link.classes.has('is-complete') && !link.classes.has('is-current')));
});

test('depth is relative to the shallowest heading, despite Hugo wrapping every h2', () => {
  const { links } = fixture();
  assert.deepEqual(links.map((link) => link.attrs['data-depth']), DEPTHS.map(String));
});

test('each section shows its own reading time, skipping collapsed admonitions', () => {
  const { links } = fixture();
  assert.deepEqual(links.map(timeLabel), ['1 min', '1 min', '1 min', '1 min']);
  assert.equal(spokenLabel(links[1]), ', 1 minute');
});

test('a heading inside a wrapper still starts its own section', () => {
  const { links } = fixture();
  // Without the wrapper check, the h3's words would land in the previous section.
  assert.equal(timeLabel(links[2]), '1 min');
  assert.equal(timeLabel(links[1]), '1 min');
});

test('the rail is capped at the first and last tracked sections, ignoring orphan links', () => {
  const { links, orphanLink } = fixture({ orphan: true });
  assert.ok(links[0].classes.has('is-first'));
  assert.ok(links[3].classes.has('is-last'));
  assert.ok(!orphanLink.classes.has('is-last'));
});

test('scrolling past a heading completes earlier sections and counts minutes left by words', () => {
  const f = fixture();
  scrollTo(f, [-400, 80, 480, 880]);
  assert.ok(f.links[0].classes.has('is-complete'));
  assert.equal(f.links[1].attrs['aria-current'], 'location');
  assert.ok(!f.links[2].classes.has('is-complete') && !f.links[2].classes.has('is-current'));
  // 50 + 213 + 10% of 215 words read out of 904: 31%, 619 words (3 min) left.
  assert.equal(f.progress.textContent, '3 min left');
  assert.equal(f.meter.attrs['aria-valuenow'], '31');
  assert.equal(f.meter.style.props['--agenda-progress'], '31%');
});

test('a hidden heading is never treated as passed', () => {
  const f = fixture();
  f.state.hidden[1] = true;
  scrollTo(f, [-400, 900, 1300, 1700]);
  assert.equal(f.links[0].attrs['aria-current'], 'location');
  assert.ok(!f.links[1].classes.has('is-current'));
});

test('jumping to a later anchor and scrolling back reverses completion', () => {
  const f = fixture();
  f.state.positions = [-800, -400, -200, 80];
  f.events.hashchange();
  assert.ok(f.links.slice(0, 3).every((link) => link.classes.has('is-complete')));
  assert.equal(f.links[3].attrs['aria-current'], 'location');
  scrollTo(f, [80, 480, 680, 880]);
  assert.equal(f.links[0].attrs['aria-current'], 'location');
  assert.ok(f.links.every((link) => !link.classes.has('is-complete')));
});

test('passing the article end completes all sections, and restoration resets them', () => {
  const f = fixture();
  scrollTo(f, [-1000, -600, -400, -200], { bottom: 100 });
  assert.ok(f.links.every((link) => link.classes.has('is-complete')));
  assert.ok(f.links.every((link) => !link.attrs['aria-current']));
  assert.equal(f.progress.textContent, 'Finished');
  assert.equal(f.meter.attrs['aria-valuenow'], '100');
  f.state.positions = [400, 800, 1000, 1200];
  f.state.bottom = 1600;
  f.events.pageshow();
  assert.ok(f.links.every((link) => !link.classes.has('is-complete')));
  assert.equal(f.progress.textContent, '4 min read');
});

test('reaching the bottom of the page finishes a post with a short footer', () => {
  const f = fixture();
  f.window.scrollY = 9100;
  // The last heading can't reach the reading line and the article ends below it.
  scrollTo(f, [-1000, -600, -400, 300], { bottom: 700 });
  assert.equal(f.progress.textContent, 'Finished');
  assert.ok(f.links.every((link) => link.classes.has('is-complete')));
});

test('the mobile bar appears once the agenda scrolls away and mirrors the current section', () => {
  const f = fixture({ isDesktop: false, withBar: true });
  const { bar } = f;
  assert.equal(bar.hidden, false);
  assert.ok(f.document.body.children.includes(bar), 'bar is mounted on body, outside .toc');
  assert.ok(!bar.classes.has('is-visible'));
  scrollTo(f, [-400, 80, 480, 880], { agendaBottom: -50 });
  assert.ok(bar.classes.has('is-visible'));
  assert.equal(bar.attrs.inert, undefined);
  assert.equal(bar.parts.meta.textContent, 'Section 2 of 4 · 3 min left');
  assert.equal(bar.parts.title.textContent, 'Build the lab');
  assert.equal(bar.parts.fill.style.props['--agenda-progress'], '31%');
  const copies = bar.parts.links.children[0].copies;
  assert.ok(copies[0].classes.has('is-complete'));
  assert.equal(copies[1].attrs['aria-current'], 'location');
  assert.equal(copies[2].attrs['data-depth'], '1', 'copies keep their depth');
  // Scrolling past the article body hides it again.
  scrollTo(f, [-400, 80, 480, 880], { bottom: -10 });
  assert.ok(!bar.classes.has('is-visible'));
  assert.equal(bar.attrs.inert, '');
});

test('the mobile bar tucks while scrolling down and returns on scroll up', () => {
  const f = fixture({ isDesktop: false, withBar: true });
  scrollTo(f, [-400, 80, 480, 880], { agendaBottom: -50 });
  f.window.scrollY = 400;
  scrollTo(f, [-500, -20, 380, 780]);
  assert.ok(f.bar.classes.has('is-tucked'));
  f.window.scrollY = 380;
  scrollTo(f, [-480, 0, 400, 800]);
  assert.ok(!f.bar.classes.has('is-tucked'));
});

test('the mobile bar stays hidden on desktop', () => {
  const f = fixture({ isDesktop: true, withBar: true });
  scrollTo(f, [-400, 80, 480, 880], { agendaBottom: -50 });
  assert.ok(!f.bar.classes.has('is-visible'));
});

test('the mobile agenda opens from the bar and closes with Escape, the backdrop or a link', () => {
  const f = fixture({ isDesktop: false, withBar: true });
  scrollTo(f, [-400, 80, 480, 880], { agendaBottom: -50 });
  const { toggle, panel } = f.bar.parts;
  toggle.listeners.click();
  assert.equal(toggle.attrs['aria-expanded'], 'true');
  assert.equal(panel.hidden, false);
  assert.equal(f.backdrop.hidden, false);
  f.documentEvents.keydown({ key: 'Escape', preventDefault() {} });
  assert.equal(toggle.attrs['aria-expanded'], 'false');
  assert.equal(panel.hidden, true);
  assert.equal(f.backdrop.hidden, true);
  assert.equal(toggle.focused, true);
  assert.deepEqual({ ...toggle.focusOptions }, { preventScroll: true });
  toggle.listeners.click();
  f.backdrop.listeners.click();
  assert.equal(panel.hidden, true);
  toggle.listeners.click();
  f.bar.parts.links.children[0].copies[3].listeners.click();
  assert.equal(panel.hidden, true);
});

test('tabbing out of the bar closes the panel', () => {
  const f = fixture({ isDesktop: false, withBar: true });
  scrollTo(f, [-400, 80, 480, 880], { agendaBottom: -50 });
  f.bar.parts.toggle.listeners.click();
  f.bar.listeners.focusout({ relatedTarget: el('a') });
  assert.equal(f.bar.parts.panel.hidden, true);
});

test('crossing to the desktop breakpoint closes an open panel', () => {
  const f = fixture({ isDesktop: false, withBar: true });
  scrollTo(f, [-400, 80, 480, 880], { agendaBottom: -50 });
  f.bar.parts.toggle.listeners.click();
  f.media.matches = true;
  f.events.resize();
  assert.equal(f.bar.parts.panel.hidden, true);
  assert.ok(!f.bar.classes.has('is-visible'));
});

test('pages without an agenda do not require browser listeners', () => {
  assert.doesNotThrow(() => vm.runInNewContext(source, {
    document: { querySelector: () => null },
  }));
});
