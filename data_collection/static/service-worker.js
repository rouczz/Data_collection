const CACHE_NAME = "farmer-app-v1";
const STATIC_URLS = [
    "/",
    "/create_farmer/",
    "/add-farm/",
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css", // Bootstrap CSS
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js",
    "/static/js/farmer.js", // Farmer-specific JS
    "/static/css/style.css", // Custom CSS
    "/static/offline.html", // Offline fallback page
];

// Install Event: Cache static assets
self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return Promise.all(
                STATIC_URLS.map(url => 
                    cache.add(url).catch(err => {
                        console.error(`Failed to cache ${url}:`, err.message);
                    })
                )
            );
        })
    );
});

// Fetch Event: Serve cached resources when offline
self.addEventListener("fetch", (event) => {
    if (event.request.method !== "GET" || event.request.url.startsWith("chrome-extension")) {
        return;
    }

    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) {
                return cachedResponse;
            }
            return fetch(event.request).catch(() => caches.match("/static/offline.html"));
        })
    );
});

// const CACHE_NAME = "kisanmitra-cache-v1";
// const STATIC_URLS = [
//   // Django URL patterns
//   "/",
//   "/create_farmer/",
//   "/dashboard/",
//   "/add_farm/1/",  // Specific example, replace with actual URL patterns
//   "/add_farm/<int:farmer_id>/",  // Generic pattern if applicable
//   '/add-plantation/<int:farmer_id>/',
//   '/add-species/<int:farmer_id>/',
//   "/upload-media/<int:farmer_id>/",
//   "/add-farm/template/",
//   "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css", // Bootstrap CSS
//   "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js",

//   // Static files
//   "/static/css/style.css",
//   "/static/js/app.js",
//   "/static/icons/image.png",
//   "/static/icons/image copy.png",
//   "/static/offline.html",  // Corrected path for offline page

//   // External library CSS and JS
//   '/static/css/bootstrap.min.css',
//   '/static/js/bootstrap.bundle.min.js',
//   'https://unpkg.com/leaflet@1.9.3/dist/leaflet.css',
//   'https://unpkg.com/leaflet@1.9.3/dist/leaflet.js',
//   'https://cdnjs.cloudflare.com/ajax/libs/idb/7.1.1/idb.min.js',
// ];

// // Install Event: Pre-cache static assets
// self.addEventListener('install', (event) => {
//   event.waitUntil(
//     caches.open(CACHE_NAME)
//       .then((cache) => {
//         console.log('[Service Worker] Caching static assets');
//         return cache.addAll(STATIC_URLS)
//           .then(() => {
//             console.log('[Service Worker] All static assets cached successfully');
//           })
//           .catch((error) => {
//             console.error('[Service Worker] Caching failed:', error);
            
//             // Attempt to cache URLs individually for more granular error tracking
//             return Promise.all( 
//               STATIC_URLS.map(url => 
//                 cache.add(url).catch(err => {
//                   console.error(`Failed to cache ${url}:`, err);
//                 })
//               )
//             );
//           });
//       })
//   );
// });

// // Fetch Event: Advanced caching strategy
// self.addEventListener('fetch', (event) => {
//   // Ignore non-GET requests and chrome-extension requests
//   if (event.request.method !== 'GET' || event.request.url.startsWith('chrome-extension')) {
//     return;
//   }

//   // HTML pages: Network-first strategy
//   if (event.request.headers.get('Accept')?.includes('text/html')) {
//     event.respondWith(
//       fetch(event.request)
//         .then(networkResponse => {
//           // Clone and cache successful HTML responses
//           if (networkResponse && networkResponse.status === 200) {
//             const responseToCache = networkResponse.clone();
//             caches.open(CACHE_NAME).then(cache => {
//               cache.put(event.request, responseToCache)
//                 .catch(err => console.error('Caching HTML failed:', err));
//             });
//           }
//           return networkResponse;
//         })
//         .catch(() => {
//           // Fallback to cached version or offline page
//           return caches.match(event.request)
//             .then(cachedResponse => {
//               if (cachedResponse) return cachedResponse;
//               return caches.match('/static/offline.html') 
//                 || new Response('Offline', { status: 503 });
//             });
//         })
//     );
//   } 
//   // Static assets: Cache-first strategy
//   else {
//     event.respondWith(
//       caches.match(event.request)
//         .then(cachedResponse => {
//           if (cachedResponse) {
//             return cachedResponse;
//           }

//           return fetch(event.request)
//             .then(networkResponse => {
//               // Cache successful responses
//               if (networkResponse && networkResponse.status === 200) {
//                 const responseToCache = networkResponse.clone();
//                 caches.open(CACHE_NAME).then(cache => {
//                   cache.put(event.request, responseToCache)
//                     .catch(err => console.error('Caching asset failed:', err));
//                 });
//               }
//               return networkResponse;
//             })
//             .catch(() => {
//               // Fallback for offline assets
//               console.log('Offline asset request:', event.request.url);
//               return new Response('Resource Unavailable', { status: 404 });
//             });
//         })
//     );
//   }
// });

// // Activation Event: Clean up old caches
// self.addEventListener('activate', (event) => {
//   event.waitUntil(
//     caches.keys().then(cacheNames => {
//       return Promise.all(
//         cacheNames.map(cacheName => {
//           if (cacheName !== CACHE_NAME) {
//             return caches.delete(cacheName);
//           }
//         })
//       );
//     }).then(() => self.clients.claim())
//   );
// });