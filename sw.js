/**
 * STUR Physics Lab - Service Worker
 * Provides offline support, caching, and background sync
 *
 * Cache Strategy:
 * - Shell (HTML, CSS, JS): Cache-first with network fallback
 * - CDN Resources (MathJax, Fonts): Stale-while-revalidate
 * - PDFs: Cache on demand
 * - Images: Cache-first
 */

const CACHE_VERSION = 'stur-v2.5.0';
const CACHE_NAME = `stur-cache-${CACHE_VERSION}`;

// Core shell files - always cache these
const SHELL_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/about.html',
  '/sitemap.html',
  '/assets/css/stur-core.css',
  '/assets/css/stur-glass.css',
  '/assets/css/stur-icons.css',
  '/assets/css/stur-index.css',
  '/assets/css/stur-theory.css',
  '/assets/js/stur-ui.js',
  '/assets/js/stur-definitions.js',
  '/assets/js/stur-version.js',
  '/assets/js/stur-mathjax-config.js',
  '/assets/js/stur-sw-register.js',
  '/assets/4.13.png'
];

// Theory pages - cache on navigation
const THEORY_PAGES = [
  '/scripts/stur_core_theory.html',
  '/scripts/stur_predictions.html',
  '/scripts/stur_falsification.html',
  '/scripts/stur_symbols.html',
  '/scripts/stur_glossary.html',
  '/scripts/stur_faq.html',
  '/scripts/stur_simulations_hub.html'
];

// CDN resources to cache
const CDN_RESOURCES = [
  'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js'
];

// Install event - cache shell assets
self.addEventListener('install', (event) => {
  console.log('[SW] Installing STUR Service Worker...');

  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[SW] Caching shell assets');
        return cache.addAll(SHELL_ASSETS);
      })
      .then(() => {
        console.log('[SW] Shell assets cached successfully');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('[SW] Failed to cache shell assets:', error);
      })
  );
});

// Activate event - clean old caches
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating STUR Service Worker...');

  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((name) => name.startsWith('stur-cache-') && name !== CACHE_NAME)
            .map((name) => {
              console.log('[SW] Deleting old cache:', name);
              return caches.delete(name);
            })
        );
      })
      .then(() => {
        console.log('[SW] Old caches cleaned');
        return self.clients.claim();
      })
  );
});

// Fetch event - serve from cache with network fallback
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // Skip chrome-extension and other non-http(s) requests
  if (!url.protocol.startsWith('http')) {
    return;
  }

  // Strategy based on request type
  if (isShellAsset(url)) {
    // Shell assets: Cache-first
    event.respondWith(cacheFirst(request));
  } else if (isCDNResource(url)) {
    // CDN resources: Stale-while-revalidate
    event.respondWith(staleWhileRevalidate(request));
  } else if (isTheoryPage(url)) {
    // Theory pages: Network-first with cache fallback
    event.respondWith(networkFirst(request));
  } else if (isPDF(url)) {
    // PDFs: Cache on demand
    event.respondWith(cacheOnDemand(request));
  } else if (isImage(url)) {
    // Images: Cache-first
    event.respondWith(cacheFirst(request));
  } else {
    // Default: Network-first
    event.respondWith(networkFirst(request));
  }
});

// Cache-first strategy
async function cacheFirst(request) {
  const cached = await caches.match(request);
  if (cached) {
    return cached;
  }

  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    console.error('[SW] Cache-first fetch failed:', error);
    return offlineFallback(request);
  }
}

// Network-first strategy
async function networkFirst(request) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    const cached = await caches.match(request);
    if (cached) {
      return cached;
    }
    return offlineFallback(request);
  }
}

// Stale-while-revalidate strategy
async function staleWhileRevalidate(request) {
  const cached = await caches.match(request);

  const fetchPromise = fetch(request)
    .then((response) => {
      if (response.ok) {
        const cache = caches.open(CACHE_NAME);
        cache.then((c) => c.put(request, response.clone()));
      }
      return response;
    })
    .catch(() => cached);

  return cached || fetchPromise;
}

// Cache on demand strategy
async function cacheOnDemand(request) {
  const cached = await caches.match(request);
  if (cached) {
    return cached;
  }

  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    console.error('[SW] Failed to fetch on demand:', error);
    return new Response('Resource unavailable offline', { status: 503 });
  }
}

// Offline fallback
function offlineFallback(request) {
  const url = new URL(request.url);

  // Return offline page for HTML requests
  if (request.headers.get('Accept')?.includes('text/html')) {
    return caches.match('/offline.html') || new Response(
      `<!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Offline - STUR Physics Lab</title>
        <style>
          body {
            background: #0a0a0f;
            color: #e5e7eb;
            font-family: system-ui, sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            text-align: center;
          }
          .offline-container {
            max-width: 400px;
            padding: 2rem;
          }
          h1 { color: #4ade80; margin-bottom: 1rem; }
          p { color: #9ca3af; line-height: 1.6; }
          .retry-btn {
            background: #4ade80;
            color: #0a0a0f;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 1.5rem;
          }
          .retry-btn:hover { background: #22c55e; }
        </style>
      </head>
      <body>
        <div class="offline-container">
          <h1>You're Offline</h1>
          <p>STUR Physics Lab requires an internet connection to load new content. Previously viewed pages may still be available.</p>
          <button class="retry-btn" onclick="location.reload()">Try Again</button>
        </div>
      </body>
      </html>`,
      { headers: { 'Content-Type': 'text/html' } }
    );
  }

  return new Response('Offline', { status: 503 });
}

// Helper functions
function isShellAsset(url) {
  return SHELL_ASSETS.some((asset) => url.pathname === asset || url.pathname.endsWith(asset));
}

function isCDNResource(url) {
  return url.hostname.includes('jsdelivr.net') ||
         url.hostname.includes('googleapis.com') ||
         url.hostname.includes('gstatic.com');
}

function isTheoryPage(url) {
  return url.pathname.startsWith('/scripts/') && url.pathname.endsWith('.html');
}

function isPDF(url) {
  return url.pathname.endsWith('.pdf');
}

function isImage(url) {
  return /\.(png|jpg|jpeg|gif|webp|svg|ico)$/i.test(url.pathname);
}

// Message handler for cache management
self.addEventListener('message', (event) => {
  if (event.data.action === 'skipWaiting') {
    self.skipWaiting();
  }

  if (event.data.action === 'clearCache') {
    caches.delete(CACHE_NAME).then(() => {
      console.log('[SW] Cache cleared');
      event.ports[0].postMessage({ success: true });
    });
  }

  if (event.data.action === 'getCacheSize') {
    getCacheSize().then((size) => {
      event.ports[0].postMessage({ size });
    });
  }
});

// Get total cache size
async function getCacheSize() {
  const cache = await caches.open(CACHE_NAME);
  const keys = await cache.keys();
  let totalSize = 0;

  for (const request of keys) {
    const response = await cache.match(request);
    if (response) {
      const blob = await response.blob();
      totalSize += blob.size;
    }
  }

  return totalSize;
}

console.log('[SW] STUR Service Worker loaded');
