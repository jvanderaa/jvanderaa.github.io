const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const { test } = require('node:test');

const source = fs.readFileSync(`${__dirname}/../assets/js/reading-agenda.js`, 'utf8');

function fixture() {
  const events = {};
  const state = { positions: [400, 800, 1200], bottom: 1600 };
  const content = { getBoundingClientRect: () => ({ bottom: state.bottom }) };
  const links = state.positions.map((_, index) => {
    const link = { hash: `#section-${index}`, classes: new Set(), attrs: {} };
    link.classList = { toggle: (name, enabled) => enabled ? link.classes.add(name) : link.classes.delete(name) };
    link.setAttribute = (name, value) => { link.attrs[name] = value; };
    link.removeAttribute = (name) => { delete link.attrs[name]; };
    return link;
  });
  const headings = links.map((_, index) => ({
    getBoundingClientRect: () => ({ top: state.positions[index] }),
    closest: () => content,
  }));
  const progress = { hidden: true, setAttribute() {} };
  const agenda = {
    open: true,
    querySelectorAll: () => links,
    querySelector: () => progress,
    closest: () => null,
    addEventListener: (name, callback) => { events[`agenda:${name}`] = callback; },
  };
  const window = {
    innerHeight: 900,
    matchMedia: () => ({ matches: true, addEventListener() {} }),
    requestAnimationFrame: (callback) => callback(),
    addEventListener: (name, callback) => { events[name] = callback; },
  };
  const document = {
    querySelector: () => agenda,
    getElementById: (id) => headings[Number(id.slice(8))],
  };
  vm.runInNewContext(source, { window, document });
  return { state, links, progress, events };
}

test('the introduction leaves every section upcoming', () => {
  const { links, progress } = fixture();
  assert.equal(progress.textContent, '0 / 3');
  assert.ok(links.every(link => !link.classes.size));
});

test('scrolling past a heading completes only earlier sections', () => {
  const { state, links, events, progress } = fixture();
  state.positions = [-400, 80, 480];
  events.scroll();
  assert.ok(links[0].classes.has('is-complete'));
  assert.equal(links[1].attrs['aria-current'], 'location');
  assert.ok(!links[2].classes.size);
  assert.equal(progress.textContent, '1 / 3');
});

test('jumping to a later anchor and scrolling back reverses completion', () => {
  const { state, links, events } = fixture();
  state.positions = [-800, -400, 80];
  events.hashchange();
  assert.ok(links[0].classes.has('is-complete'));
  assert.ok(links[1].classes.has('is-complete'));
  assert.equal(links[2].attrs['aria-current'], 'location');
  state.positions = [80, 480, 880];
  events.scroll();
  assert.equal(links[0].attrs['aria-current'], 'location');
  assert.ok(links.every(link => !link.classes.has('is-complete')));
  assert.equal(links[2].attrs['aria-current'], undefined);
});

test('passing the article end completes all sections, and restoration resets them', () => {
  const { state, links, events, progress } = fixture();
  state.positions = [-1000, -600, -200];
  state.bottom = 100;
  events.scroll();
  assert.ok(links.every(link => link.classes.has('is-complete')));
  assert.ok(links.every(link => !link.attrs['aria-current']));
  assert.equal(progress.textContent, '3 / 3');
  state.positions = [400, 800, 1200];
  state.bottom = 1600;
  events.pageshow();
  assert.ok(links.every(link => !link.classes.size));
  assert.equal(progress.textContent, '0 / 3');
});

test('pages without an agenda do not require browser listeners', () => {
  assert.doesNotThrow(() => vm.runInNewContext(source, {
    document: { querySelector: () => null },
  }));
});
