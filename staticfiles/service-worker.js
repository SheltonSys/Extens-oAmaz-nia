const CACHE_NAME = 'extensao-cache-v1';
const urlsToCache = [
  '/',
  '/static/assets/custom.css',
  '/static/assets/plugins/jquery/jquery.min.js',
  '/static/assets/dist/css/adminlte.min.css',
  '/static/assets/plugins/bootstrap/js/bootstrap.bundle.min.js',
  '/static/assets/plugins/fontawesome-free/css/all.min.css',
  '/static/assets/icons/icon-192.png',
  '/static/assets/icons/icon-512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(urlsToCache);
    })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames =>
      Promise.all(
        cacheNames
          .filter(name => name !== CACHE_NAME)
          .map(name => caches.delete(name))
      )
    )
  );
});
