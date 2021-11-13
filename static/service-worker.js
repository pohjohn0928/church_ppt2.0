const cacheName = 'pwa';
const filesToCache = [
    '/calvary',
    '/static/images/icons/icon-192x192.png'
];

self.addEventListener('install', (e) => {
  // console.log('[ServiceWorker] Install');
  e.waitUntil((async () => {
    const cache = await caches.open(cacheName)
    // console.log('[ServiceWorker] Caching app shell');
    await cache.addAll(filesToCache);
  })());
});

self.addEventListener('fetch', (e) => {
  // console.log('[ServiceWorker] Fetch', e.request.url);
  e.respondWith(
    caches.match(e.request).then(response => {
        return response || fetch(e.request);
    })
  );
});