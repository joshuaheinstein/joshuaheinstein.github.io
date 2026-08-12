/* ==========================================================================
   Joshua Heinstein — portfolio behaviour
   Vanilla JS, no dependencies. Everything degrades gracefully without it:
   the page renders fully, defaulting to the technical framing.
   ========================================================================== */
(function () {
  'use strict';

  var root = document.documentElement;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Small storage helper (private browsing can throw) ---------- */
  function store(key, value) {
    try {
      if (value === undefined) return localStorage.getItem(key);
      localStorage.setItem(key, value);
    } catch (e) { /* ignore */ }
    return null;
  }

  /* ---------------------------------------------------------------- *
   * Positioning mode — "technical", "general", or "deck"
   *
   * technical/general are two framings of the same page; deck swaps the page
   * for the deep-dive section. All three are just a class on <html> — the CSS
   * does the rest, and every mode's content stays in the DOM.
   * ---------------------------------------------------------------- */
  var MODES = ['technical', 'general', 'deck'];
  var modeButtons = Array.prototype.slice.call(document.querySelectorAll('.mode-btn'));

  function applyMode(mode, animate) {
    if (MODES.indexOf(mode) === -1) mode = 'technical';

    // Suppress reveal transitions during the swap so already-visible
    // content doesn't flash back in from the bottom.
    if (!animate) root.classList.add('mode-swapping');

    MODES.forEach(function (m) {
      root.classList.toggle('mode-' + m, m === mode);
    });

    modeButtons.forEach(function (btn) {
      btn.setAttribute('aria-pressed', String(btn.dataset.mode === mode));
    });

    // Newly shown content should be visible immediately, not stuck at opacity 0.
    document.querySelectorAll('.reveal').forEach(function (el) {
      if (isInViewport(el)) el.classList.add('in');
    });

    if (!animate) {
      requestAnimationFrame(function () {
        requestAnimationFrame(function () { root.classList.remove('mode-swapping'); });
      });
    }

    store('jh-mode', mode);
  }

  function isInViewport(el) {
    var r = el.getBoundingClientRect();
    return r.top < window.innerHeight && r.bottom > 0;
  }

  modeButtons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var was = currentMode();
      var now = btn.dataset.mode;
      applyMode(now, false);
      countUpVisible();

      // Entering or leaving deck mode replaces the page contents rather than
      // reframing them, so a preserved scroll position lands nowhere useful.
      if (was !== now && (was === 'deck' || now === 'deck')) {
        window.scrollTo(reduceMotion ? { top: 0 } : { top: 0, behavior: 'smooth' });
      }
    });
  });

  function currentMode() {
    for (var i = 0; i < MODES.length; i++) {
      if (root.classList.contains('mode-' + MODES[i])) return MODES[i];
    }
    return 'technical';
  }

  var savedMode = store('jh-mode');
  if (savedMode && savedMode !== 'technical') applyMode(savedMode, false);

  /* ---------------------------------------------------------------- *
   * Color theme
   * ---------------------------------------------------------------- */
  var themeBtn = document.getElementById('theme-btn');
  var savedTheme = store('jh-theme');
  if (savedTheme === 'dark' || savedTheme === 'light') root.setAttribute('data-theme', savedTheme);

  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var current = root.getAttribute('data-theme');
      if (!current) {
        current = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      }
      var next = current === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      store('jh-theme', next);
    });
  }

  /* ---------------------------------------------------------------- *
   * Reveal on scroll
   * ---------------------------------------------------------------- */
  var revealEls = Array.prototype.slice.call(document.querySelectorAll('.reveal'));

  if (reduceMotion || !('IntersectionObserver' in window)) {
    revealEls.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('in');
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    revealEls.forEach(function (el) { io.observe(el); });

    // Hero is above the fold — show it right away.
    document.querySelectorAll('.hero .reveal').forEach(function (el) {
      el.classList.add('in');
      io.unobserve(el);
    });
  }

  /* ---------------------------------------------------------------- *
   * Animated stat counters
   * ---------------------------------------------------------------- */
  function countUp(el) {
    if (el.dataset.done === '1') return;
    var target = parseFloat(el.dataset.count);
    if (isNaN(target)) return;
    el.dataset.done = '1';

    var prefix = el.dataset.prefix || '';
    var suffix = el.dataset.suffix || '';

    if (reduceMotion) { el.innerHTML = prefix + target + suffix; return; }

    var start = performance.now();
    var duration = 1100;

    function frame(now) {
      var t = Math.min((now - start) / duration, 1);
      var eased = 1 - Math.pow(1 - t, 3);          // ease-out cubic
      el.innerHTML = prefix + Math.round(target * eased) + suffix;
      if (t < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  function countUpVisible() {
    document.querySelectorAll('.stat-n[data-count]').forEach(function (el) {
      if (el.offsetParent !== null && isInViewport(el)) countUp(el);
    });
  }

  if ('IntersectionObserver' in window) {
    var statIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) countUp(entry.target);
      });
    }, { threshold: 0.5 });
    document.querySelectorAll('.stat-n[data-count]').forEach(function (el) { statIO.observe(el); });
  }

  /* ---------------------------------------------------------------- *
   * Nav: blur-on-scroll, scroll progress, active section
   * ---------------------------------------------------------------- */
  var nav = document.getElementById('nav');
  var progress = document.getElementById('progress');
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.nav-links a'));
  var sections = navLinks
    .map(function (a) { return document.querySelector(a.getAttribute('href')); })
    .filter(Boolean);

  var ticking = false;

  function onScroll() {
    var y = window.scrollY || window.pageYOffset;

    if (nav) nav.classList.toggle('stuck', y > 12);

    if (progress) {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.transform = 'scaleX(' + (max > 0 ? Math.min(y / max, 1) : 0) + ')';
    }

    // Active nav link = last section whose top has passed the nav line.
    var activeIndex = -1;
    sections.forEach(function (sec, i) {
      if (sec.getBoundingClientRect().top <= 90) activeIndex = i;
    });
    navLinks.forEach(function (a, i) { a.classList.toggle('active', i === activeIndex); });

    ticking = false;
  }

  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
  }, { passive: true });

  window.addEventListener('resize', onScroll, { passive: true });
  onScroll();

  /* ---------------------------------------------------------------- *
   * Footer year
   * ---------------------------------------------------------------- */
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
