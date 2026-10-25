/* Shared behaviour: theme, nav, search palette, reveal, reading progress, toc highlight */
(function () {
  'use strict';
  const root = document.documentElement;
  const siteRoot = (document.querySelector('meta[name="site-root"]') || {}).content || '';
  const $ = (s, el) => (el || document).querySelector(s);
  const $$ = (s, el) => Array.from((el || document).querySelectorAll(s));

  // ---- theme
  const themeBtn = $('#theme-btn');
  function currentTheme() {
    const t = root.getAttribute('data-theme');
    if (t && t !== 'auto') return t;
    return matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  themeBtn && themeBtn.addEventListener('click', () => {
    const next = currentTheme() === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('theme', next); } catch (e) {}
  });

  // ---- nav
  const toggle = $('.nav-toggle'), menu = $('#nav-menu');
  toggle && toggle.addEventListener('click', () => {
    const open = menu.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
  });
  $$('.has-dd > .nav-link').forEach(btn => {
    const li = btn.parentElement;
    btn.addEventListener('click', e => {
      e.preventDefault();
      const open = li.getAttribute('aria-expanded') === 'true';
      $$('.has-dd[aria-expanded="true"]').forEach(x => { if (x !== li) { x.setAttribute('aria-expanded', 'false'); x.querySelector('.nav-link').setAttribute('aria-expanded', 'false'); } });
      li.setAttribute('aria-expanded', String(!open));
      btn.setAttribute('aria-expanded', String(!open));
    });
  });
  document.addEventListener('click', e => {
    if (!e.target.closest('.has-dd')) $$('.has-dd[aria-expanded="true"]').forEach(x => { x.setAttribute('aria-expanded', 'false'); x.querySelector('.nav-link').setAttribute('aria-expanded', 'false'); });
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { $$('.has-dd[aria-expanded="true"]').forEach(x => x.setAttribute('aria-expanded', 'false')); closePalette(); } });

  // ---- reading progress
  const bar = $('#read-progress');
  if (bar) {
    const upd = () => {
      const h = document.documentElement;
      const max = h.scrollHeight - h.clientHeight;
      bar.style.width = max > 0 ? Math.min(100, (h.scrollTop / max) * 100) + '%' : '0%';
    };
    addEventListener('scroll', upd, { passive: true }); upd();
  }

  // ---- reveal on scroll
  const io = 'IntersectionObserver' in window ? new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } }), { rootMargin: '0px 0px -8% 0px' }) : null;
  $$('.reveal').forEach(el => io ? io.observe(el) : el.classList.add('in'));

  // ---- toc highlight
  const tocLinks = $$('.toc a[href^="#"]');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    const map = new Map();
    tocLinks.forEach(a => { const t = $(a.getAttribute('href')); if (t) map.set(t, a); });
    const obs = new IntersectionObserver(es => {
      es.forEach(en => { if (en.isIntersecting) { tocLinks.forEach(a => a.classList.remove('on')); map.get(en.target).classList.add('on'); } });
    }, { rootMargin: '-20% 0px -70% 0px' });
    map.forEach((a, t) => obs.observe(t));
  }

  // ---- search palette
  const pal = $('#palette'), q = $('#palette-q'), list = $('#palette-list');
  let index = null, sel = 0, results = [];
  function openPalette() {
    if (!pal) return;
    pal.hidden = false; q.value = ''; list.innerHTML = '<li class="ps">Type to search…</li>'; setTimeout(() => q.focus(), 10);
    if (!index) fetch(siteRoot + 'search.json').then(r => r.json()).then(j => { index = j; }).catch(() => { index = []; });
  }
  function closePalette() { if (pal && !pal.hidden) pal.hidden = true; }
  $('#search-btn') && $('#search-btn').addEventListener('click', openPalette);
  document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); pal && pal.hidden ? openPalette() : closePalette(); }
    if (e.key === '/' && !/input|textarea|select/i.test(document.activeElement.tagName) && pal && pal.hidden) { e.preventDefault(); openPalette(); }
  });
  pal && pal.addEventListener('click', e => { if (e.target === pal) closePalette(); });
  function score(item, terms) {
    const hay = (item.t + ' ' + item.s + ' ' + (item.g || '') + ' ' + item.k).toLowerCase();
    let s = 0;
    for (const t of terms) {
      if (!t) continue;
      if (item.t.toLowerCase().startsWith(t)) s += 8;
      else if (item.t.toLowerCase().includes(t)) s += 5;
      else if (hay.includes(t)) s += 2;
      else return 0;
    }
    return s;
  }
  function render() {
    if (!index) return;
    let raw = q.value.trim().toLowerCase();
    let kind = null;
    if (raw.startsWith('t:')) { kind = 'tool'; raw = raw.slice(2).trim(); }
    if (raw.startsWith('d:')) { kind = 'department'; raw = raw.slice(2).trim(); }
    const terms = raw.split(/\s+/).filter(Boolean);
    results = index.map(it => ({ it, s: terms.length ? score(it, terms) : 1 }))
      .filter(x => x.s > 0 && (!kind || x.it.k.toLowerCase().includes(kind)))
      .sort((a, b) => b.s - a.s).slice(0, 12).map(x => x.it);
    sel = 0;
    list.innerHTML = results.length ? results.map((r, i) => `<li role="option" class="${i === 0 ? 'on' : ''}" data-i="${i}"><span class="pt">${esc(r.t)}</span><span class="pk">${esc(r.k)}</span><span class="ps">${esc(r.s)}</span></li>`).join('') : '<li class="ps">No matches.</li>';
  }
  function go(i) { const r = results[i]; if (r) location.href = siteRoot + r.u; }
  q && q.addEventListener('input', render);
  q && q.addEventListener('keydown', e => {
    if (e.key === 'ArrowDown') { sel = Math.min(sel + 1, results.length - 1); mark(); e.preventDefault(); }
    if (e.key === 'ArrowUp') { sel = Math.max(sel - 1, 0); mark(); e.preventDefault(); }
    if (e.key === 'Enter') { go(sel); }
  });
  list && list.addEventListener('click', e => { const li = e.target.closest('li[data-i]'); if (li) go(+li.dataset.i); });
  function mark() { $$('#palette-list li').forEach((li, i) => li.classList.toggle('on', i === sel)); const on = $('#palette-list li.on'); on && on.scrollIntoView({ block: 'nearest' }); }
  function esc(s) { return String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); }

  // expose small helpers for page scripts
  window.AIH = { siteRoot, esc, $, $$ };
})();
/* Remember closed first-visit guides; department finder on the home page */
(function () {
  document.querySelectorAll('details.guide').forEach(d => {
    const k = 'aih-guide-' + d.id;
    try { if (localStorage.getItem(k) === 'closed') d.open = false; } catch (e) {}
    d.addEventListener('toggle', () => { try { localStorage.setItem(k, d.open ? 'open' : 'closed'); } catch (e) {} });
  });
  const f = document.getElementById('dept-finder');
  if (f) f.addEventListener('change', () => { if (f.value) location.href = (document.querySelector('meta[name="site-root"]') || {}).content + f.value; });
})();
