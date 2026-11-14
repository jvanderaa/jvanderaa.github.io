/* Enhance Hugo's native contents links; navigation also works without JavaScript. */
(() => {
  const agenda = document.querySelector('[data-reading-agenda]');
  if (!agenda) return;

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
  const desktop = window.matchMedia('(min-width: 1024px)');
  let scheduled = false;
  let previousState = '';

  function update() {
    scheduled = false;
    // Match the heading scroll margin and leave room above the reading position.
    const readingLine = Math.min(120, window.innerHeight * 0.25);
    let current = -1;
    entries.forEach(({ heading }, index) => {
      if (heading.getBoundingClientRect().top <= readingLine) current = index;
    });
    const finished = current === entries.length - 1 && content &&
      content.getBoundingClientRect().bottom <= readingLine;
    const state = `${current}:${Boolean(finished)}`;
    if (state === previousState) return;
    previousState = state;

    entries.forEach(({ link }, index) => {
      const active = index === current && !finished;
      link.classList.toggle('is-complete', index < current || Boolean(finished));
      link.classList.toggle('is-current', active);
      if (active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
    if (progress) {
      const completed = finished ? entries.length : Math.max(0, current);
      progress.hidden = false;
      progress.textContent = `${completed} / ${entries.length}`;
      progress.setAttribute('aria-label', `${completed} of ${entries.length} sections passed`);
    }

    // Keep the active link visible in a long desktop agenda, without moving the page.
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
