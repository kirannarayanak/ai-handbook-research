/* Side-by-side comparison of tools or departments */
(function () {
  const D = JSON.parse(document.getElementById('compare-data').textContent);
  const { esc, siteRoot } = window.AIH;
  const q = document.getElementById('cmp-q'), sug = document.getElementById('cmp-suggest'), selWrap = document.getElementById('cmp-selected');
  const table = document.getElementById('cmp-table'), empty = document.getElementById('cmp-empty'), presets = document.getElementById('presets');
  const MAX = 4;
  const params = new URLSearchParams(location.search);
  let mode = params.has('d') ? 'depts' : 'tools';
  let sel = (params.get(mode === 'tools' ? 't' : 'd') || '').split(',').filter(Boolean).slice(0, MAX);
  if (mode === 'tools' && !params.has('t')) sel = ['claude', 'gemini', 'microsoft-365-copilot'];

  const ROWS = {
    tools: [
      ['Vendor', t => esc(t.v)], ['Family', t => esc(t.g)],
      ['Confidence', t => `<span class="badge badge-conf-${t.c}">${t.c}</span>`],
      ['Handbook departments', t => `<b>${t.nd}</b> of 60`],
      ['What it is', t => esc(t.what)],
      ['Key capabilities', t => '<ul>' + t.caps.map(c => `<li>${esc(c)}</li>`).join('') + '</ul>'],
      ['Enterprise data handling', t => esc(t.data)],
      ['Licensing and pricing', t => esc(t.price)],
      ['Integrations', t => esc(t.integ)],
      ['2025-2026 developments', t => esc(t.dev)],
      ['Best-fit departments', t => esc(t.fit)],
      ['Training notes', t => esc(t.train)],
      ['Caveats', t => esc(t.cav)],
      ['Profile', t => `<a href="${siteRoot}tools/${t.s}/">Open full profile →</a>`],
    ],
    depts: [
      ['Cluster', d => esc(d.cl)],
      ['Tier', d => `<span class="badge badge-tier-${d.tier.toLowerCase()}">${d.tier}</span>`],
      ['Confidence', d => `<span class="badge badge-conf-${d.c}">${d.c}</span>`],
      ['Workplace application', d => esc(d.app)],
      ['Recommended tools', d => '<ul>' + d.tools.map(x => `<li>${esc(x)}</li>`).join('') + '</ul>'],
      ['Capstone deliverable', d => esc(d.cap)],
      ['Data risks and rules', d => esc(d.risk)],
      ['Adoption KPIs', d => esc(d.kpi)],
      ['Curriculum emphasis', d => esc(d.cur)],
      ['Profile', d => `<a href="${siteRoot}departments/${d.s}/">Open full profile →</a>`],
    ],
  };
  const items = () => D[mode];
  const byS = s => items().find(x => x.s === s);

  function render() {
    document.querySelectorAll('[data-mode]').forEach(b => b.classList.toggle('on', b.dataset.mode === mode));
    presets.style.display = mode === 'tools' ? '' : 'none';
    q.placeholder = mode === 'tools' ? 'Add a tool…' : 'Add a department…';
    const chosen = sel.map(byS).filter(Boolean);
    selWrap.innerHTML = chosen.map(x => `<span class="chip on">${esc(x.n)} <button class="x" data-rm="${x.s}" aria-label="Remove">✕</button></span>`).join('') + (chosen.length < MAX ? `<span class="muted small">${MAX - chosen.length} more can be added</span>` : '');
    const p = new URLSearchParams(); if (sel.length) p.set(mode === 'tools' ? 't' : 'd', sel.join(',')); history.replaceState(null, '', location.pathname + (sel.length ? '?' + p : ''));
    if (chosen.length < 2) { table.innerHTML = ''; empty.hidden = false; return; }
    empty.hidden = true;
    table.innerHTML = '<thead><tr><th>Attribute</th>' + chosen.map(x => `<th>${esc(x.n)}<button class="rm" data-rm="${x.s}" aria-label="Remove">✕</button></th>`).join('') + '</tr></thead><tbody>' +
      ROWS[mode].map(([label, fn]) => `<tr><td>${label}</td>${chosen.map(x => `<td>${fn(x)}</td>`).join('')}</tr>`).join('') + '</tbody>';
  }
  document.addEventListener('click', e => {
    const rm = e.target.closest('[data-rm]'); if (rm) { sel = sel.filter(s => s !== rm.dataset.rm); render(); }
    const pm = e.target.closest('[data-mode]'); if (pm && pm.dataset.mode !== mode) { mode = pm.dataset.mode; sel = mode === 'tools' ? ['claude', 'gemini', 'microsoft-365-copilot'] : ['01-office-of-the-ceo', '20-financial-planning-analysis']; render(); }
    const pr = e.target.closest('[data-preset]'); if (pr) { sel = pr.dataset.preset.split(','); render(); }
    if (!e.target.closest('.cmp-search')) sug.hidden = true;
  });
  let cur = 0, matches = [];
  function suggest() {
    const v = q.value.trim().toLowerCase();
    matches = items().filter(x => !sel.includes(x.s) && (!v || x.n.toLowerCase().includes(v) || (x.v || x.cl || '').toLowerCase().includes(v))).slice(0, 10);
    cur = 0;
    sug.innerHTML = matches.map((x, i) => `<li data-s="${x.s}" class="${i === 0 ? 'on' : ''}"><span>${esc(x.n)}</span><span class="muted small">${esc(x.v || x.tier || '')}</span></li>`).join('') || '<li class="muted">No matches</li>';
    sug.hidden = false;
  }
  function add(s) { if (sel.length >= MAX) sel = sel.slice(1); sel.push(s); q.value = ''; sug.hidden = true; render(); }
  q.addEventListener('input', suggest); q.addEventListener('focus', suggest);
  q.addEventListener('keydown', e => {
    if (e.key === 'ArrowDown') { cur = Math.min(cur + 1, matches.length - 1); paint(); e.preventDefault(); }
    if (e.key === 'ArrowUp') { cur = Math.max(cur - 1, 0); paint(); e.preventDefault(); }
    if (e.key === 'Enter' && matches[cur]) { add(matches[cur].s); e.preventDefault(); }
    if (e.key === 'Escape') sug.hidden = true;
  });
  function paint() { sug.querySelectorAll('li').forEach((li, i) => li.classList.toggle('on', i === cur)); }
  sug.addEventListener('click', e => { const li = e.target.closest('li[data-s]'); if (li) add(li.dataset.s); });
  render();
})();
