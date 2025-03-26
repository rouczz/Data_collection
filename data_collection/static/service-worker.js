// const CACHE_NAME = "kisanmitra-cache-v6";
// const STATIC_URLS = [
//   "/",
//   "/add_farm/<int:farmer_id>",
//   "/static/css/style.css",
//   "/static/js/app.js",
//   "/static/icons/image.png",
//   "/static/icons/image copy.png",
//   "templates/offline.html",
//   '/static/css/bootstrap.min.css',
//   '/static/js/bootstrap.bundle.min.js',
//   'https://unpkg.com/leaflet@1.9.3/dist/leaflet.css',
//   'https://unpkg.com/leaflet@1.9.3/dist/leaflet.js',
//   'https://cdnjs.cloudflare.com/ajax/libs/idb/7.1.1/idb.min.js',
// ];

// // Install Event: Cache Static Assets
// self.addEventListener("install", (event) => {
//   event.waitUntil(
//     caches.open(CACHE_NAME)
//       .then((cache) => {
//         console.log(`[Service Worker] Attempting to pre-cache static URLs`);
//         return cache.addAll(STATIC_URLS)
//           .then(() => {
//             console.log(`[Service Worker] Successfully pre-cached all static URLs`);
//           })
//           .catch((error) => {
//             console.error(`[Service Worker] Error pre-caching static URLs:`, error);
//             // Log each URL that failed to cache
//             STATIC_URLS.forEach(url => {
//               cache.add(url).catch(err => {
//                 console.error(`Failed to cache URL: ${url}`, err);
//               });
//             });
//           });
//       })
//   );
// });

// self.addEventListener("fetch", (event) => {
//   // Check if the request is for an HTML page
//   const isHtmlRequest = 
//     event.request.mode === "navigate" || 
//     (event.request.method === "GET" && 
//      event.request.headers.get("accept")?.includes("text/html"));

//   if (isHtmlRequest) {
//     event.respondWith(
//       (async () => {
//         try {
//           // Attempt network fetch first
//           const networkResponse = await fetch(event.request);
          
//           // Log successful network fetch
//           console.log(`[Service Worker] Network fetch successful for: ${event.request.url}`);

//           // Clone and cache the response
//           const cache = await caches.open(CACHE_NAME);
//           const responseToCache = networkResponse.clone();
          
//           try {
//             await cache.put(event.request, responseToCache);
//             console.log(`[Service Worker] Cached HTML page: ${event.request.url}`);
//           } catch (cacheError) {
//             console.error(`[Service Worker] Error caching HTML page: ${event.request.url}`, cacheError);
//           }

//           return networkResponse;
//         } catch (networkError) {
//           // Network fetch failed, try cache
//           console.warn(`[Service Worker] Network fetch failed for: ${event.request.url}`, networkError);

//           const cachedResponse = await caches.match(event.request);
          
//           if (cachedResponse) {
//             console.log(`[Service Worker] Serving cached HTML page: ${event.request.url}`);
//             return cachedResponse;
//           }

//           // No cache available
//           console.error(`[Service Worker] No cached version available for: ${event.request.url}`);
          
//           // Serve offline page
//           return caches.match('/offline.html') || 
//                  new Response('Offline. Please check your connection.', { 
//                    status: 503, 
//                    headers: { 'Content-Type': 'text/html' } 
//                  });
//         }
//       })()
//     );
//   }
// });

// // Debugging: Log all cache contents
// async function debugCaches() {
//   const cacheNames = await caches.keys();
//   console.log('[Service Worker] Existing Caches:', cacheNames);

//   for (const cacheName of cacheNames) {
//     const cache = await caches.open(cacheName);
//     const keys = await cache.keys();
//     console.log(`[Service Worker] Contents of ${cacheName}:`, 
//       keys.map(request => request.url)
//     );
//   }
// }

// self.addEventListener('activate', (event) => {
//   event.waitUntil(debugCaches());
// });


// // Activate Event: Clear Old Caches


const CACHE_NAME = "kisanmitra-cache-v1";
const STATIC_URLS = [
  // Django URL patterns
  "/",
  "/create_farmer/",
  "/dashboard/",
  "/add_farm/1/",  // Specific example, replace with actual URL patterns
  "/add_farm/<int:farmer_id>/",  // Generic pattern if applicable
  '/add-plantation/<int:farmer_id>/',
  '/add-species/<int:farmer_id>/',
  "/upload-media/<int:farmer_id>/",

  // Static files
  "/static/css/style.css",
  "/static/js/app.js",
  "/static/icons/image.png",
  "/static/icons/image copy.png",
  "/static/offline.html",  // Corrected path for offline page

  // External library CSS and JS
  '/static/css/bootstrap.min.css',
  '/static/js/bootstrap.bundle.min.js',
  'https://unpkg.com/leaflet@1.9.3/dist/leaflet.css',
  'https://unpkg.com/leaflet@1.9.3/dist/leaflet.js',
  'https://cdnjs.cloudflare.com/ajax/libs/idb/7.1.1/idb.min.js',
];

// Install Event: Pre-cache static assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[Service Worker] Caching static assets');
        return cache.addAll(STATIC_URLS)
          .then(() => {
            console.log('[Service Worker] All static assets cached successfully');
          })
          .catch((error) => {
            console.error('[Service Worker] Caching failed:', error);
            
            // Attempt to cache URLs individually for more granular error tracking
            return Promise.all( 
              STATIC_URLS.map(url => 
                cache.add(url).catch(err => {
                  console.error(`Failed to cache ${url}:`, err);
                })
              )
            );
          });
      })
  );
});

// Fetch Event: Advanced caching strategy
self.addEventListener('fetch', (event) => {
  // Ignore non-GET requests and chrome-extension requests
  if (event.request.method !== 'GET' || event.request.url.startsWith('chrome-extension')) {
    return;
  }

  // HTML pages: Network-first strategy
  if (event.request.headers.get('Accept')?.includes('text/html')) {
    event.respondWith(
      fetch(event.request)
        .then(networkResponse => {
          // Clone and cache successful HTML responses
          if (networkResponse && networkResponse.status === 200) {
            const responseToCache = networkResponse.clone();
            caches.open(CACHE_NAME).then(cache => {
              cache.put(event.request, responseToCache)
                .catch(err => console.error('Caching HTML failed:', err));
            });
          }
          return networkResponse;
        })
        .catch(() => {
          // Fallback to cached version or offline page
          return caches.match(event.request)
            .then(cachedResponse => {
              if (cachedResponse) return cachedResponse;
              return caches.match('/static/offline.html') 
                || new Response('Offline', { status: 503 });
            });
        })
    );
  } 
  // Static assets: Cache-first strategy
  else {
    event.respondWith(
      caches.match(event.request)
        .then(cachedResponse => {
          if (cachedResponse) {
            return cachedResponse;
          }

          return fetch(event.request)
            .then(networkResponse => {
              // Cache successful responses
              if (networkResponse && networkResponse.status === 200) {
                const responseToCache = networkResponse.clone();
                caches.open(CACHE_NAME).then(cache => {
                  cache.put(event.request, responseToCache)
                    .catch(err => console.error('Caching asset failed:', err));
                });
              }
              return networkResponse;
            })
            .catch(() => {
              // Fallback for offline assets
              console.log('Offline asset request:', event.request.url);
              return new Response('Resource Unavailable', { status: 404 });
            });
        })
    );
  }
});

// Activation Event: Clean up old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});