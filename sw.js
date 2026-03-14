// sw.js — Matheux Service Worker
const CACHE_NAME = 'matheux-v1';
const CACHE_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/scree.png',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
  'https://cdn.tailwindcss.com',
  'https://fonts.googleapis.com/css2?family=Syne:wght@700;800;900&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&display=swap'
];

// Installation : cache les assets statiques
self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll(CACHE_ASSETS.map(url => new Request(url, { mode: 'no-cors' })));
    })
  );
  self.skipWaiting();
});

// Activation : nettoyer les anciens caches
self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(
        keys.filter(function(k) { return k !== CACHE_NAME; })
            .map(function(k) { return caches.delete(k); })
      );
    })
  );
  self.clients.claim();
});

// Fetch : Network First pour GAS (toujours frais), Cache First pour assets
self.addEventListener('fetch', function(e) {
  var url = e.request.url;

  // GAS API → toujours réseau, jamais cache
  if (url.includes('script.google.com')) {
    e.respondWith(
      fetch(e.request).catch(function() {
        return new Response(
          JSON.stringify({ status: 'error', message: 'offline' }),
          { headers: { 'Content-Type': 'application/json' } }
        );
      })
    );
    return;
  }

  // Assets statiques → Cache First avec fallback réseau
  e.respondWith(
    caches.match(e.request).then(function(cached) {
      return cached || fetch(e.request).then(function(response) {
        // Mettre en cache les nouvelles ressources statiques
        if (response.ok && e.request.method === 'GET') {
          var clone = response.clone();
          caches.open(CACHE_NAME).then(function(cache) {
            cache.put(e.request, clone);
          });
        }
        return response;
      }).catch(function() {
        // Offline → page offline si navigation
        if (e.request.mode === 'navigate') {
          return caches.match('/offline.html') || caches.match('/index.html');
        }
      });
    })
  );
});

// Notifications push (infra prête, désactivée en prod)
self.addEventListener('push', function(e) {
  if (!e.data) return;
  var data = e.data.json();
  e.waitUntil(
    self.registration.showNotification(data.title || 'Matheux', {
      body: data.body || 'Ton boost du jour t\'attend ! ⚡',
      icon: '/icons/icon-192.png',
      badge: '/icons/icon-96.png',
      tag: 'matheux-boost',
      data: { url: data.url || '/' }
    })
  );
});

self.addEventListener('notificationclick', function(e) {
  e.notification.close();
  e.waitUntil(clients.openWindow(e.notification.data.url || '/'));
});
