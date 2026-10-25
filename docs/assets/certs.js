/* Filter certification rows by kind */
(function () {
  const segs = document.querySelectorAll('#filters .seg button[data-kind]');
  const rows = Array.from(document.querySelectorAll('tr[data-kind]'));
  segs.forEach(b => b.addEventListener('click', () => {
    segs.forEach(x => x.classList.remove('on')); b.classList.add('on');
    const k = b.dataset.kind;
    rows.forEach(r => r.classList.toggle('hidden', k && r.dataset.kind !== k));
    document.querySelectorAll('.cert-card').forEach(c => c.classList.toggle('hidden', k && !c.querySelector('tr[data-kind]:not(.hidden)')));
  }));
})();
