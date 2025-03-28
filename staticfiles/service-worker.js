const CACHE_NAME = "farmer-app-v2";
const STATIC_CACHE_URLS = [
    "/create_farmer/",
    "/add-farm/",
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css", 
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js",
    "/static/js/farmer.js", 
    "/static/js/farm.js",
    "/static/css/style.css", 
    "/static/offline.html", 
];

// Debugging function
function debugLog(message, ...args) {
    console.log(`[SW Debug] ${message}`, ...args);
}

self.addEventListener("install", (event) => {
    debugLog("Installing service worker");
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return Promise.all(
                STATIC_CACHE_URLS.map(url => {
                    return fetch(url, {
                        method: 'GET',
                        headers: {
                            'Cache-Control': 'no-cache'
                        }
                    }).then(response => {
                        if (response.ok) {
                            debugLog(`Caching ${url}`);
                            return cache.put(url, response);
                        }
                        debugLog(`Failed to cache ${url}`);
                        return Promise.resolve();
                    }).catch(error => {
                        debugLog(`Error caching ${url}:`, error);
                        return Promise.resolve();
                    });
                })
            );
        })
    );
    self.skipWaiting();
});

self.addEventListener("activate", (event) => {
    debugLog("Activating service worker");
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        debugLog(`Deleting old cache: ${cacheName}`);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => {
            debugLog("Claiming clients");
            return self.clients.claim();
        })
    );
});

self.addEventListener("fetch", (event) => {
    // Ignore non-GET requests and chrome-extension URLs
    if (event.request.method !== "GET" || event.request.url.startsWith("chrome-extension")) {
        return;
    }

    // Special handling for HTML pages
    if (event.request.headers.get('Accept')?.includes('text/html')) {
        event.respondWith(
            caches.open(CACHE_NAME).then((cache) => {
                return fetch(event.request, {
                    headers: {
                        'Cache-Control': 'no-cache'
                    }
                }).then((networkResponse) => {
                    // Only cache successful HTML responses
                    if (networkResponse.ok && networkResponse.type === 'basic') {
                        const responseToCache = networkResponse.clone();
                        cache.put(event.request, responseToCache);
                    }
                    return networkResponse;
                }).catch(() => {
                    // Fallback to cached response
                    return cache.match(event.request) || 
                           caches.match("/static/offline.html") || 
                           new Response('Offline', { 
                               status: 503, 
                               headers: { 'Content-Type': 'text/plain' } 
                           });
                });
            })
        );
        return;
    }

    // Default fetch strategy for other resources
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            return cachedResponse || fetch(event.request);
        })
    );
});
// const CACHE_NAME = "farmer-app-v1";
// const OFFLINE_URL = '/offline.html'
// const STATIC_URLS = [
//     "/create_farmer/",
//     "/add-farm/",
//     "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css", 
//     "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js",
//     "/static/js/farmer.js", 
//     "/static/js/farm.js",
//     "/static/css/style.css", 
//     "/static/offline.html", 
// ];

// // install event
// // Install event: cache static assets
// self.addEventListener('install', event => {
//     event.waitUntil(
//       caches.open(CACHE_NAME)
//         .then(cache => {
//           console.log('Opened cache');
//           return cache.addAll(STATIC_URLS);
//         })
//     );
//   });
  
//   // Fetch event: serve from cache if possible
//   self.addEventListener('fetch', event => {
//     event.respondWith(
//       caches.match(event.request)
//         .then(response => {
//           // If a cached file exists, return it; otherwise, fetch from network
//           return response || fetch(event.request);
//         })
//     );
//   });
  
//   // Activate event: cleanup old caches
//   self.addEventListener('activate', event => {
//     const cacheWhitelist = [CACHE_NAME];
//     event.waitUntil(
//       caches.keys().then(cacheNames => {
//         return Promise.all(
//           cacheNames.map(cacheName => {
//             if (!cacheWhitelist.includes(cacheName)) {
//               return caches.delete(cacheName);
//             }
//           })
//         );
//       })
//     );
//   });
  
// // Install Event: Comprehensive Caching
// self.addEventListener("install", (event) => {
//     console.log("[ServiceWorker] Install");
//     event.waitUntil(
//         caches.open(CACHE_NAME).then((cache) => {
//             console.log("[ServiceWorker] Caching app shell");
//             return cache.addAll(STATIC_URLS.map(url => new Request(url, { 
//                 cache: 'no-cache',  // Ensure fresh network fetch
//                 credentials: 'same-origin'  // Include credentials for same-origin requests
//             })));
//         }).catch(error => {
//             console.error("[ServiceWorker] Caching failed:", error);
//         })
//     );
    
//     // Force the waiting service worker to become active
//     self.skipWaiting();
// });

// // Activate Event: Clean up old caches and claim clients
// self.addEventListener("activate", (event) => {
//     console.log("[ServiceWorker] Activate");
//     event.waitUntil(
//         caches.keys().then((cacheNames) => {
//             return Promise.all(
//                 cacheNames.map((cacheName) => {
//                     if (cacheName !== CACHE_NAME) {
//                         console.log("[ServiceWorker] Removing old cache:", cacheName);
//                         return caches.delete(cacheName);
//                     }
//                 })
//             );
//         }).then(() => {
//             console.log("[ServiceWorker] Claiming clients");
//             return self.clients.claim();
//         })
//     );
// });

// // Fetch Event: Advanced Network-First Strategy
// self.addEventListener("fetch", (event) => {
//     // Ignore non-GET requests and chrome-extension URLs
//     if (event.request.method !== "GET" || event.request.url.startsWith("chrome-extension")) {
//         return;
//     }

//     event.respondWith(
//         // Network-first strategy with cache fallback
//         fetch(event.request).catch(() => {
//             // If network request fails, try cache
//             return caches.match(event.request).then((response) => {
//                 if (response) {
//                     return response;
//                 }
                
//                 // If specific request not in cache, handle differently based on Accept header
//                 if (event.request.headers.get('Accept').includes('text/html')) {
//                     // Fallback to offline page for HTML requests
//                     return caches.match("/static/offline.html");
//                 }
                
//                 // For other resources, return a network error response
//                 return new Response('Offline', { 
//                     status: 503, 
//                     headers: { 'Content-Type': 'text/plain' } 
//                 });
//             });
//         })
//     );
// });

// // Handle PWA install prompt
// self.addEventListener('beforeinstallprompt', (event) => {
//     console.log("[ServiceWorker] Install prompt prevented");
//     event.preventDefault();
//     // Optionally store the event for later use
//     self.deferredPrompt = event;
// });

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