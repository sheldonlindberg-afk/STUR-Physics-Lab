// The old STUR v7 service worker is retired. This replacement clears any
// caches it left behind and unregisters itself, so visitors get the live site.
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    for (const key of await caches.keys()) await caches.delete(key);
    await self.registration.unregister();
    for (const client of await self.clients.matchAll()) client.navigate(client.url);
  })());
});
