/* Interactive coverage matrix */
(function () {
  const D = JSON.parse(document.getElementById('matrix-data').textContent);
  const { esc, siteRoot } = window.AIH;
  const grid = document.getElementById('matrix'), panel = document.getElementById('m-panel'), legend = document.getElementById('legend'), summary = document.getElementById('m-summary');
  const selG = document.getElementById('m-group'), selC = document.getElementById('m-cluster'), horiz = document.getElementById('m-horiz');
  const state = { view: 'high', tier: '', group: '', cluster: '', hideHoriz: false, hl: null };
  D.groups.forEach((g, i) => selG.insertAdjacentHTML('beforeend', `<option value="${i}">${esc(g)}</option>`));
  D.clusters.forEach((c, i) => selC.insertAdjacentHTML('beforeend', `<option value="${i}">${esc(c)}</option>`));
  const params = new URLSearchParams(location.search);
  if (params.get('tool') || params.get('dept')) state.view = 'detail';
  if (params.get('tool')) state.hl = { tool: params.get('tool') };
  if (params.get('dept')) state.hl = { dept: parseInt(params.get('dept'), 10) };

  function visibleDepts() { return D.depts.filter(d => (!state.tier || d.t === state.tier) && (state.cluster === '' || d.c === +state.cluster)); }
  function visibleTools() { return D.tools.map((t, i) => ({ ...t, i })).filter(t => (state.group === '' || t.g === +state.group) && !(state.hideHoriz && t.g === 0)); }

  function renderHigh() {
    const depts = visibleDepts(), tools = visibleTools();
    const toolSet = new Set(tools.map(t => t.i));
    const cl = [...new Set(depts.map(d => d.c))], gr = [...new Set(tools.map(t => t.g))];
    const counts = {}; let max = 1;
    const members = {};
    depts.forEach(d => d.tools.forEach(ti => { if (!toolSet.has(ti)) return; const g = D.tools[ti].g, k = d.c + ':' + g; counts[k] = (counts[k] || 0) + 1; (members[k] = members[k] || []).push([d, ti]); if (counts[k] > max) max = counts[k]; }));
    grid.style.gridTemplateColumns = `max-content repeat(${gr.length}, 96px)`;
    let h = '<div class="corner"></div>' + gr.map(g => `<div class="mh high">${esc(D.groups[g])}</div>`).join('');
    cl.forEach(c => {
      h += `<a class="rh" href="${siteRoot}departments/#${slug(D.clusters[c])}">${esc(D.clusters[c])} <small>${depts.filter(d => d.c === c).length}</small></a>`;
      gr.forEach(g => { const n = counts[c + ':' + g] || 0; const a = n ? 0.15 + 0.85 * (n / max) : 0; h += `<div class="cell high" data-k="${c}:${g}" style="background:${n ? `color-mix(in srgb, var(--accent) ${Math.round(a * 100)}%, var(--bg-2))` : 'transparent'};color:${a > 0.55 ? '#fff' : 'var(--fg)'}" role="gridcell" tabindex="0" aria-label="${esc(D.clusters[c])} × ${esc(D.groups[g])}: ${n}">${n || ''}</div>`; });
    });
    grid.innerHTML = h;
    legend.innerHTML = `<span><i style="background:color-mix(in srgb,var(--accent) 15%,var(--bg-2))"></i>few</span><span><i style="background:color-mix(in srgb,var(--accent) 60%,var(--bg-2))"></i>some</span><span><i style="background:var(--accent)"></i>many</span><span class="muted">Number = department-tool recommendations in the handbook</span>`;
    summary.textContent = `${depts.length} departments × ${tools.length} tools, aggregated into ${cl.length} clusters × ${gr.length} families.`;
    grid.querySelectorAll('.cell.high').forEach(el => el.addEventListener('click', () => {
      const m = members[el.dataset.k] || [];
      if (!m.length) { panel.hidden = true; return; }
      const [c, g] = el.dataset.k.split(':').map(Number);
      const byDept = new Map(); m.forEach(([d, ti]) => { if (!byDept.has(d.n)) byDept.set(d.n, { d, t: [] }); byDept.get(d.n).t.push(D.tools[ti]); });
      panel.hidden = false;
      panel.innerHTML = `<h3>${esc(D.clusters[c])} × ${esc(D.groups[g])}</h3><p class="muted small">${m.length} recommendations across ${byDept.size} departments.</p>` +
        [...byDept.values()].map(({ d, t }) => `<p><a href="${siteRoot}departments/${d.s}/"><b>${pad(d.n)} ${esc(d.name)}</b></a> <span class="badge badge-tier-${d.t.toLowerCase()}">${d.t}</span><br><span class="chips">${t.map(x => `<a class="chip chip-xs" href="${siteRoot}tools/${x.s}/">${esc(x.n)}</a>`).join('')}</span></p>`).join('');
      panel.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }));
  }

  function renderDetail() {
    const depts = visibleDepts(), tools = visibleTools();
    grid.style.gridTemplateColumns = `max-content repeat(${tools.length}, 28px)`;
    let h = '<div class="corner"></div>' + tools.map(t => `<a class="mh ${state.hl && state.hl.tool === t.s ? 'hl' : ''}" href="${siteRoot}tools/${t.s}/" title="${esc(t.n)}">${esc(t.n)}</a>`).join('');
    depts.forEach(d => {
      const set = new Set(d.tools);
      const rowHl = state.hl && state.hl.dept === d.n;
      h += `<a class="rh" href="${siteRoot}departments/${d.s}/" style="${rowHl ? 'color:var(--accent);font-weight:700' : ''}"><small>${pad(d.n)}</small>${esc(d.name)}</a>`;
      tools.forEach(t => {
        const on = set.has(t.i);
        const dim = state.hl && !((state.hl.tool && state.hl.tool === t.s) || (state.hl.dept && state.hl.dept === d.n));
        h += `<div class="cell ${on ? 'on' : ''} ${dim ? 'dim' : ''}" data-d="${d.n}" data-t="${t.i}" role="gridcell" tabindex="0" aria-label="${pad(d.n)} ${esc(d.name)} × ${esc(t.n)}: ${on ? 'recommended' : 'not listed'}"></div>`;
      });
    });
    grid.innerHTML = h;
    legend.innerHTML = `<span><i style="background:var(--accent)"></i>recommended in the handbook</span><span><i></i>not listed</span>${state.hl ? '<button class="chip chip-btn" id="clear-hl">Clear highlight</button>' : ''}`;
    summary.textContent = `${depts.length} departments × ${tools.length} tools · ${depts.reduce((s, d) => s + d.tools.filter(ti => tools.some(t => t.i === ti)).length, 0)} recommendations.`;
    const c = document.getElementById('clear-hl'); c && c.addEventListener('click', () => { state.hl = null; history.replaceState(null, '', location.pathname); render(); });
    grid.querySelectorAll('.cell').forEach(el => {
      const open = () => {
        const d = D.depts.find(x => x.n === +el.dataset.d), t = D.tools[+el.dataset.t];
        panel.hidden = false;
        panel.innerHTML = `<h3>${pad(d.n)} ${esc(d.name)} × ${esc(t.n)}</h3><p>${el.classList.contains('on') ? 'The handbook recommends this tool for this department.' : 'Not in the handbook\'s list for this department.'}</p><div class="chips"><a class="chip" href="${siteRoot}departments/${d.s}/">Open department</a><a class="chip" href="${siteRoot}tools/${t.s}/">Open tool</a><a class="chip" href="${siteRoot}compare/?t=${t.s}">Compare tool</a></div>`;
      };
      el.addEventListener('click', open);
      el.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } });
    });
    if (state.hl) {
      const target = state.hl.tool ? grid.querySelector('.mh.hl') : grid.querySelector(`.cell[data-d="${state.hl.dept}"]`);
      target && setTimeout(() => target.scrollIntoView({ block: 'nearest', inline: 'center' }), 50);
    }
  }

  function render() { panel.hidden = true; state.view === 'high' ? renderHigh() : renderDetail(); }
  function pad(n) { return String(n).padStart(2, '0'); }
  function slug(s) { return s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''); }

  document.querySelectorAll('.matrix-controls .seg button').forEach(b => b.addEventListener('click', () => {
    b.parentElement.querySelectorAll('button').forEach(x => x.classList.remove('on')); b.classList.add('on');
    if ('view' in b.dataset) state.view = b.dataset.view;
    if ('tier' in b.dataset) state.tier = b.dataset.tier;
    render();
  }));
  document.querySelectorAll('.matrix-controls [data-view]').forEach(b => b.classList.toggle('on', b.dataset.view === state.view));
  selG.addEventListener('change', () => { state.group = selG.value; render(); });
  selC.addEventListener('change', () => { state.cluster = selC.value; render(); });
  horiz.addEventListener('change', () => { state.hideHoriz = horiz.checked; render(); });
  render();
})();
