/* Filter the source lists */
(function () {
  const f = document.getElementById('src-filter'); if (!f) return;
  const items = Array.from(document.querySelectorAll('.srcs li'));
  f.addEventListener('input', () => {
    const v = f.value.trim().toLowerCase();
    items.forEach(li => li.classList.toggle('hidden', v && !li.textContent.toLowerCase().includes(v)));
    document.querySelectorAll('.src-group').forEach(d => { const any = d.querySelector('li:not(.hidden)'); d.classList.toggle('hidden', !any); if (v) d.open = true; });
  });
})();
