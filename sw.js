// sw.js — Matheux Service Worker
// v14 (25/09/2026) : les pages HTML ne sont PLUS servies depuis le cache en priorité.
//  - navigations / documents HTML → réseau d'abord (cache: 'no-store'), cache seulement hors ligne ;
//    ainsi une ancienne landing ou une ancienne app ne peut plus être resservie après une mise en ligne.
//  - API (Supabase, GAS, /api) et toute requête non-GET → jamais interceptées ni mises en cache.
//  - ressources statiques du même domaine (icônes, images, js, css) → cache, rafraîchi en arrière-plan.
//  - cross-origin (CDN, polices) → laissé au navigateur (pas de réponses opaques en cache).
// À chaque changement de ce fichier : monter CACHE_NAME (l'activation supprime les anciens caches).
const CACHE_NAME = 'matheux-v14';
// Uniquement des fichiers qui existent dans le dépôt (un seul 404 ferait échouer toute l'installation).
const CACHE_ASSETS = [
  '/offline.html',
  '/manifest.json',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
  '/icons/favicon-32.png',
  '/assets/mark-navy.png'
];

self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE_NAME)
      .then(function (cache) { return cache.addAll(CACHE_ASSETS.map(function (u) { return new Request(u, { cache: 'reload' }); })); })
      .then(function () { return self.skipWaiting(); })
  );
});

// Activation : supprime TOUS les anciens caches (dont matheux-v13 qui contenait app.html et la landing)
self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys()
      .then(function (keys) {
        return Promise.all(keys.filter(function (k) { return k !== CACHE_NAME; }).map(function (k) { return caches.delete(k); }));
      })
      .then(function () { return self.clients.claim(); })
  );
});

function estHtml(req) {
  if (req.mode === 'navigate' || req.destination === 'document') return true;
  var accept = req.headers.get('accept') || '';
  return accept.indexOf('text/html') !== -1;
}

self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return; // POST (API, paiement…) : le navigateur gère, rien en cache
  var url = new URL(req.url);
  if (url.origin !== self.location.origin) return; // Supabase, GAS, CDN, polices : jamais interceptés
  if (url.pathname.indexOf('/api') === 0 || url.pathname.indexOf('/dev/') === 0 || url.pathname === '/sw.js') return;

  // Pages HTML : réseau d'abord, toujours frais. Cache (dernière version vue) ou offline.html si hors ligne.
  if (estHtml(req)) {
    e.respondWith(
      fetch(req, { cache: 'no-store' }).then(function (res) {
        if (res.ok && res.type === 'basic' && url.pathname.indexOf('/b/') !== 0) {
          var copie = res.clone();
          caches.open(CACHE_NAME).then(function (c) { c.put(req, copie); });
        }
        return res;
      }).catch(function () {
        return caches.match(req).then(function (hit) { return hit || caches.match('/offline.html'); });
      })
    );
    return;
  }

  // Statique même domaine : cache immédiat + mise à jour en arrière-plan (stale-while-revalidate)
  e.respondWith(
    caches.open(CACHE_NAME).then(function (cache) {
      return cache.match(req).then(function (hit) {
        var reseau = fetch(req).then(function (res) {
          if (res.ok && res.type === 'basic') cache.put(req, res.clone());
          return res;
        });
        if (hit) { e.waitUntil(reseau.catch(function () {})); return hit; }
        return reseau;
      });
    })
  );
});

// Notifications push (infra prête, désactivée en prod)
self.addEventListener('push', function (e) {
  if (!e.data) return;
  var data = e.data.json();
  e.waitUntil(
    self.registration.showNotification(data.title || 'Matheux', {
      body: data.body || 'Tes exos du jour t\'attendent.',
      icon: '/icons/icon-192.png',
      badge: '/icons/icon-96.png',
      tag: 'matheux-boost',
      data: { url: data.url || '/app.html' }
    })
  );
});

self.addEventListener('notificationclick', function (e) {
  e.notification.close();
  e.waitUntil(clients.openWindow(e.notification.data.url || '/app.html'));
});
