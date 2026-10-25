/* Learning-path progress, stored in localStorage */
(function () {
  const KEY = 'aih-progress';
  const load = () => { try { return JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { return {}; } };
  const save = p => { try { localStorage.setItem(KEY, JSON.stringify(p)); } catch (e) {} };
  const prog = load();
  const cards = document.querySelectorAll('.chapter-card[data-chapter]');
  if (cards.length) {
    let done = 0;
    cards.forEach(c => { if (prog[c.dataset.chapter]) { c.classList.add('done'); c.querySelector('.done-mark').hidden = false; done++; } });
    const bar = document.getElementById('path-bar'), txt = document.getElementById('path-text');
    if (bar) bar.style.width = (done / cards.length * 100) + '%';
    if (txt) txt.textContent = `${done} of ${cards.length} chapters done`;
  }
  const btn = document.getElementById('mark-done');
  if (btn) {
    const id = btn.dataset.chapter;
    const paint = () => {
      const d = !!prog[id];
      btn.innerHTML = (d ? '✓ Chapter done · click to undo' : btn.dataset.label || btn.innerHTML);
      btn.classList.toggle('btn-primary', !d);
    };
    btn.dataset.label = btn.innerHTML;
    paint();
    btn.addEventListener('click', () => { if (prog[id]) delete prog[id]; else prog[id] = Date.now(); save(prog); paint(); });
  }
})();
