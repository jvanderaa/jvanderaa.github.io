/* Enhance Hugo's native contents links; navigation also works without JavaScript. */
(() => {
  const agenda = document.querySelector('[data-reading-agenda]');
  if (!agenda) return;

  // Hugo's ReadingTime uses 213 words per minute for English content.
  const WORDS_PER_MINUTE = 213;

  const entries = Array.from(agenda.querySelectorAll('nav a[href^="#"]'))
    .map((link) => {
      try {
        return { link, heading: document.getElementById(decodeURIComponent(link.hash.slice(1))) };
      } catch {
        return { link, heading: null };
      }
    })
    .filter(({ heading }) => heading);
  if (!entries.length) return;

  const content = entries[0].heading.closest('.max-w-prose');
  const progress = agenda.querySelector('[data-agenda-progress]');
  const meter = agenda.querySelector('[data-agenda-meter]');
  const desktop = window.matchMedia('(min-width: 1024px)');

  // Depth relative to the shallowest entry. Hugo's startLevel = 1 wraps every h2 in an
  // empty outer list item, so nesting alone can't tell an h2 from an h3.
  function listDepth(link) {
    let depth = 0;
    for (let node = link.parentElement; node && node !== agenda; node = node.parentElement) {
      if (node.tagName === 'UL' || node.tagName === 'OL') depth += 1;
    }
    return depth;
  }
  const depths = entries.map(({ link }) => listDepth(link));
  const minDepth = Math.min(...depths);
  entries.forEach((entry, index) => {
    entry.label = entry.link.textContent.trim();
    entry.links = [entry.link];
    entry.words = 0;
    entry.link.setAttribute('data-depth', String(depths[index] - minDepth));
  });

  // Word counts per section: content blocks belong to the last heading at or above them.
  let introWords = 0;
  const headingIndex = new Map(entries.map(({ heading }, index) => [heading, index]));
  if (content) {
    let section = -1;
    Array.from(content.children).forEach((block) => {
      if (headingIndex.has(block)) {
        section = headingIndex.get(block);
      } else if (block.contains) {
        // A heading wrapped by a shortcode starts its section at this block.
        entries.forEach(({ heading }, index) => {
          if (index > section && block.contains(heading)) section = index;
        });
      }
      const words = countWords(block);
      if (section < 0) introWords += words;
      else entries[section].words += words;
    });
  }
  const totalWords = introWords + entries.reduce((sum, entry) => sum + entry.words, 0);

  function countWords(node) {
    if (node.nodeType === 3) return (node.textContent.match(/\S+/g) || []).length;
    if (node.nodeType !== 1) return 0;
    const tag = node.tagName;
    if (tag === 'SCRIPT' || tag === 'STYLE') return 0;
    // Collapsed admonitions (optional detail) stay out of the estimate; count only their title.
    if (tag === 'DETAILS' && !node.open) {
      const summary = Array.from(node.children).find((child) => child.tagName === 'SUMMARY');
      return summary ? countWords(summary) : 0;
    }
    let total = 0;
    node.childNodes.forEach((child) => { total += countWords(child); });
    return total;
  }

  function sectionTime(words) {
    const minutes = words / WORDS_PER_MINUTE;
    if (minutes < 0.5) return { text: '<1 min', spoken: 'under 1 minute' };
    const rounded = Math.round(minutes);
    return { text: `${rounded} min`, spoken: `${rounded} minute${rounded === 1 ? '' : 's'}` };
  }

  // Per-section reading time, visible to sighted readers and spoken as a phrase.
  entries.forEach((entry) => {
    const time = sectionTime(entry.words);
    const visible = document.createElement('span');
    visible.className = 'agenda-time';
    visible.setAttribute('aria-hidden', 'true');
    visible.textContent = time.text;
    const spoken = document.createElement('span');
    spoken.className = 'agenda-sr';
    spoken.textContent = `, ${time.spoken}`;
    entry.link.appendChild(visible);
    entry.link.appendChild(spoken);
  });

  // Mobile reading bar: a sticky summary that opens a copy of the agenda.
  const bar = document.querySelector('[data-reading-bar]');
  const mobile = bar ? setupBar(bar) : null;

  // The rail ends at the first and last tracked sections.
  entries[0].links.forEach((link) => link.classList.add('is-first'));
  entries[entries.length - 1].links.forEach((link) => link.classList.add('is-last'));

  let scheduled = false;
  let previousState = '';
  let previousCurrent = null;
  let lastScrollY = window.scrollY || 0;

  function minutesLeft(wordsLeft) {
    return Math.max(1, Math.round(wordsLeft / WORDS_PER_MINUTE));
  }

  // A heading inside a closed admonition or hidden panel has no boxes and can't be passed.
  function isRendered(heading) {
    return !heading.getClientRects || heading.getClientRects().length > 0;
  }

  function atPageEnd() {
    const root = document.documentElement;
    if (!root || !root.scrollHeight) return false;
    return window.innerHeight + (window.scrollY || 0) >= root.scrollHeight - 2;
  }

  function update() {
    scheduled = false;
    // Leave room above the reading position for the header and the mobile bar.
    const readingLine = Math.min(120, window.innerHeight * 0.25);
    const tops = entries.map(({ heading }) => heading.getBoundingClientRect().top);
    let current = -1;
    tops.forEach((top, index) => {
      if (top <= readingLine && isRendered(entries[index].heading)) current = index;
    });
    const contentBox = content ? content.getBoundingClientRect() : null;
    // Finished once the article ends above the reading line, or the page can't scroll further.
    const finished = Boolean(
      (current === entries.length - 1 && contentBox && contentBox.bottom <= readingLine) ||
      (current >= 0 && atPageEnd()),
    );

    // Words read: whole sections above the current one, plus the part of it already scrolled past.
    let wordsRead = 0;
    if (finished) {
      wordsRead = totalWords;
    } else if (current < 0) {
      const start = contentBox ? contentBox.top : tops[0];
      wordsRead = fraction(readingLine, start, tops[0]) * introWords;
    } else {
      wordsRead = introWords;
      for (let index = 0; index < current; index += 1) wordsRead += entries[index].words;
      const end = current + 1 < entries.length ? tops[current + 1] : (contentBox ? contentBox.bottom : tops[current]);
      wordsRead += fraction(readingLine, tops[current], end) * entries[current].words;
    }
    const percent = totalWords ? Math.round((wordsRead / totalWords) * 100) : 0;
    const left = minutesLeft(totalWords - wordsRead);

    if (mobile) mobile.place(contentBox);

    const state = `${current}:${finished}:${percent}:${left}`;
    if (state === previousState) return;
    previousState = state;

    entries.forEach(({ links }, index) => {
      const active = index === current && !finished;
      links.forEach((link) => {
        link.classList.toggle('is-complete', index < current || finished);
        link.classList.toggle('is-current', active);
        if (active) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    });

    let status = `${left} min left`;
    if (finished) status = 'Finished';
    else if (current < 0) status = `${left} min read`;

    if (progress) {
      progress.hidden = false;
      progress.textContent = status;
    }
    if (meter) {
      meter.hidden = false;
      meter.style.setProperty('--agenda-progress', `${percent}%`);
      meter.setAttribute('aria-valuenow', String(percent));
      meter.setAttribute('aria-valuetext', finished ? 'Finished' : `${percent}%, ${status}`);
    }
    if (mobile) mobile.render({ current, finished, percent, status });

    // Keep the active link visible in a long desktop agenda, without moving the page.
    if (current === previousCurrent) return;
    previousCurrent = current;
    const activeLink = entries[current]?.link;
    const scroller = agenda.closest('.toc');
    if (desktop.matches && agenda.open && activeLink && scroller) {
      const bounds = scroller.getBoundingClientRect();
      const activeBounds = activeLink.getBoundingClientRect();
      if (activeBounds.bottom > bounds.bottom - 16) {
        scroller.scrollTop += activeBounds.bottom - bounds.bottom + 16;
      } else if (activeBounds.top < bounds.top + 64) {
        scroller.scrollTop += activeBounds.top - bounds.top - 64;
      }
    }
  }

  function fraction(line, start, end) {
    const span = end - start;
    if (!(span > 0)) return line >= start ? 1 : 0;
    return Math.min(1, Math.max(0, (line - start) / span));
  }

  function setupBar(root) {
    const toggle = root.querySelector('[data-bar-toggle]');
    const panel = root.querySelector('[data-bar-panel]');
    const list = root.querySelector('[data-bar-links]');
    const meta = root.querySelector('[data-bar-meta]');
    const title = root.querySelector('[data-bar-title]');
    const fill = root.querySelector('[data-bar-fill]');
    const backdrop = document.querySelector('[data-bar-backdrop]');
    const source = agenda.querySelector('nav > ul');
    if (!toggle || !panel || !list || !source) return null;

    // Copy the agenda (without Hugo's nav id) and pair each copied link with its entry.
    // The copy keeps data-depth and the time labels added above.
    const copy = source.cloneNode(true);
    list.appendChild(copy);
    const copied = Array.from(copy.querySelectorAll('a[href^="#"]'));
    const originals = Array.from(source.querySelectorAll('a[href^="#"]'));
    copied.forEach((link, index) => {
      const entry = entries.find((item) => item.link === originals[index]);
      if (entry) entry.links.push(link);
      link.addEventListener('click', () => setOpen(false));
    });

    // Mount outside Congo's .toc: it is an in-flow scroll container on small screens, so
    // changes inside it trigger scroll anchoring and focus scrolling on the page.
    if (document.body) {
      document.body.appendChild(root);
      if (backdrop) document.body.appendChild(backdrop);
    }
    root.hidden = false;

    let visible = false;
    let open = false;

    function setOpen(next, restoreFocus) {
      if (next === open) return;
      open = next;
      toggle.setAttribute('aria-expanded', String(open));
      panel.hidden = !open;
      if (backdrop) backdrop.hidden = !open;
      root.classList.toggle('is-open', open);
      if (open) {
        root.classList.remove('is-tucked');
        // Bring the current section into view inside the panel only; scrollIntoView
        // would also scroll the page behind the fixed bar.
        const active = list.querySelector('.is-current');
        if (active && panel.getBoundingClientRect) {
          const box = panel.getBoundingClientRect();
          const item = active.getBoundingClientRect();
          if (item.top < box.top || item.bottom > box.bottom) {
            panel.scrollTop += item.top - box.top - (box.height - item.height) / 2;
          }
        }
      } else if (restoreFocus) {
        toggle.focus({ preventScroll: true });
      }
    }

    toggle.addEventListener('click', () => setOpen(!open));
    if (backdrop) backdrop.addEventListener('click', () => setOpen(false, true));
    // Escape works wherever focus is; Safari doesn't focus buttons on click.
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && open) {
        event.preventDefault();
        setOpen(false, true);
      }
    });
    // Tabbing out of the bar closes the panel rather than leaving it over the page.
    root.addEventListener('focusout', (event) => {
      if (open && event.relatedTarget && !(root.contains && root.contains(event.relatedTarget))) {
        setOpen(false);
      }
    });
    panel.querySelectorAll('[data-bar-close]').forEach((link) => {
      link.addEventListener('click', () => setOpen(false));
    });

    return {
      // Show the bar on small screens once the in-page agenda has scrolled away,
      // and only while the article body is on screen.
      place(contentBox) {
        const show = !desktop.matches && agenda.getBoundingClientRect().bottom < 0 &&
          Boolean(contentBox) && contentBox.bottom > 0;
        if (show !== visible) {
          visible = show;
          if (!show && open) {
            const hadFocus = root.contains && root.contains(document.activeElement);
            setOpen(false);
            // Focus would otherwise fall to <body> once the bar goes inert.
            const summary = agenda.querySelector('summary');
            if (hadFocus && summary && summary.focus) summary.focus({ preventScroll: true });
          }
          root.classList.toggle('is-visible', show);
          if (show) root.removeAttribute('inert');
          else root.setAttribute('inert', '');
        }
        // Tuck the bar away while scrolling down; bring it back on any scroll up.
        const y = window.scrollY || 0;
        if (Math.abs(y - lastScrollY) > 8) {
          if (!open) root.classList.toggle('is-tucked', y > lastScrollY);
          lastScrollY = y;
        }
      },
      render({ current, finished, percent, status }) {
        if (fill) fill.style.setProperty('--agenda-progress', `${percent}%`);
        if (meta) {
          meta.textContent = finished || current < 0
            ? status
            : `Section ${current + 1} of ${entries.length} · ${status}`;
        }
        if (title) {
          title.textContent = current >= 0 ? entries[current].label : (root.dataset.title || '');
        }
      },
    };
  }

  function scheduleUpdate() {
    if (!scheduled) {
      scheduled = true;
      window.requestAnimationFrame(update);
    }
  }

  // A desktop agenda stays expanded; mobile readers can collapse it normally.
  agenda.addEventListener('toggle', () => {
    if (desktop.matches && !agenda.open) agenda.open = true;
  });
  desktop.addEventListener('change', () => {
    if (desktop.matches) agenda.open = true;
    scheduleUpdate();
  });
  window.addEventListener('scroll', scheduleUpdate, { passive: true });
  window.addEventListener('resize', scheduleUpdate);
  window.addEventListener('hashchange', scheduleUpdate);
  window.addEventListener('pageshow', scheduleUpdate);
  window.addEventListener('load', scheduleUpdate);
  if (window.ResizeObserver && content) new ResizeObserver(scheduleUpdate).observe(content);
  update();
})();
