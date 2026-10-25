/* Animated counters on the home page */
(function () {
  const els = document.querySelectorAll('.stat-n[data-count]');
  if (!els.length || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const run = el => {
    const target = parseInt(el.dataset.count.replace(/[^0-9]/g, ''), 10);
    if (!target) return;
    const start = performance.now(), dur = 1100;
    const step = now => {
      const p = Math.min(1, (now - start) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * e).toLocaleString();
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  const io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { run(en.target); io.unobserve(en.target); } }));
  els.forEach(el => io.observe(el));
})();
