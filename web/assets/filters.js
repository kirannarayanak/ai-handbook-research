/* Client-side filtering for catalogue, directory and "more" pages */
(function () {
  const q = document.getElementById('filter-q');
  const segs = document.querySelectorAll('#filters .seg button');
  const lensChips = document.querySelectorAll('#lens-chips .chip-btn');
  const items = Array.from(document.querySelectorAll('[data-name]'));
  const groups = Array.from(document.querySelectorAll('.group'));
  const empty = document.getElementById('empty');
  const state = { q: '', conf: '', tier: '', lens: '' };
  function apply() {
    let shown = 0;
    items.forEach(el => {
      const ok = (!state.q || el.dataset.name.includes(state.q))
        && (!state.conf || el.dataset.conf === state.conf)
        && (!state.tier || el.dataset.tier === state.tier)
        && (!state.lens || el.dataset.lens === state.lens);
      el.classList.toggle('hidden', !ok);
      if (ok) shown++;
    });
    groups.forEach(g => g.classList.toggle('hidden', !g.querySelector('[data-name]:not(.hidden)')));
    if (empty) empty.hidden = shown > 0;
  }
  q && q.addEventListener('input', () => { state.q = q.value.trim().toLowerCase(); apply(); });
  segs.forEach(b => b.addEventListener('click', () => {
    b.parentElement.querySelectorAll('button').forEach(x => x.classList.remove('on')); b.classList.add('on');
    if ('conf' in b.dataset) state.conf = b.dataset.conf;
    if ('tier' in b.dataset) state.tier = b.dataset.tier;
    apply();
  }));
  lensChips.forEach(c => c.addEventListener('click', () => {
    lensChips.forEach(x => x.classList.remove('on')); c.classList.add('on'); state.lens = c.dataset.lens; apply();
  }));
  // open a details card when linked by hash
  if (location.hash) { const el = document.getElementById(location.hash.slice(1)); if (el && el.tagName === 'DETAILS') { el.open = true; setTimeout(() => el.scrollIntoView({ block: 'start' }), 50); } }
  addEventListener('hashchange', () => { const el = document.getElementById(location.hash.slice(1)); if (el && el.tagName === 'DETAILS') el.open = true; });
})();
