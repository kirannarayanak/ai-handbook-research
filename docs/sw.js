/* SkillGrid service worker: network-first pages, cache-first versioned assets, offline fallback */
const VERSION = 'sg-6ade4a2f';
const ASSETS = VERSION + '-assets', PAGES = VERSION + '-pages';
const ROOT = new URL(self.registration.scope).pathname;
self.addEventListener('install', e => { e.waitUntil(caches.open(PAGES).then(c => c.add(ROOT + 'offline.html')).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => !k.startsWith(VERSION)).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const req = e.request; if (req.method !== 'GET') return;
  const url = new URL(req.url);
  const sameOrigin = url.origin === location.origin;
  const isFont = /fonts\.(googleapis|gstatic)\.com$/.test(url.hostname);
  if (req.mode === 'navigate') {
    e.respondWith(fetch(req).then(r => { const copy = r.clone(); caches.open(PAGES).then(c => c.put(req, copy)); return r; })
      .catch(() => caches.match(req).then(r => r || caches.match(ROOT + 'offline.html'))));
    return;
  }
  if ((sameOrigin && (url.searchParams.has('v') || /\.(json|svg|png)$/.test(url.pathname))) || isFont) {
    e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(r => { if (r.ok) { const copy = r.clone(); caches.open(ASSETS).then(c => c.put(req, copy)); } return r; })));
  }
});
