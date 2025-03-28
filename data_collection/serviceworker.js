// Base Service Worker implementation.  To use your own Service Worker, set the PWA_SERVICE_WORKER_PATH variable in settings.py

var staticCacheName = "django-pwa-v" + new Date().getTime();
var filesToCache = [

    "/create_farmer/",
    "/add-farm/",
    "/add-plantation/",
    "/add-species/",
    "/static/js/farmer.js", 
    "/static/js/farm.js",
    "/static/css/style.css", 
    "/static/offline.html", 
    "/media-upload/",
];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from Cache
// self.addEventListener("fetch", event => {
//     event.respondWith(
//         caches.match(event.request)
//             .then(response => {
//                 return response || fetch(event.request);
//             })
//             .catch(() => {
//                 return caches.match('/static/offline.html');
//             })
//     )
// });


self.addEventListener('fetch', (event) => {
    event.respondWith(
        (async () => {
            try {
                // Create a URL without query parameters
                const url = new URL(event.request.url);
                const baseUrl = `${url.origin}${url.pathname}`;

                // Flexible cache matching strategy
                const cacheMatch = await caches.match(baseUrl, {
                    ignoreSearch: true  // Ignore query parameters
                });

                // If cache match found, return it
                if (cacheMatch) {
                    return cacheMatch;
                }

                // Try network first
                try {
                    const networkResponse = await fetch(event.request);
                    
                    // Optional: Cache successful network responses
                    if (networkResponse && networkResponse.status === 200) {
                        const cache = await caches.open('v1-cache');
                        cache.put(baseUrl, networkResponse.clone());
                    }
                    
                    return networkResponse;
                } catch (networkError) {
                    // Fallback to offline page if network fails
                    return caches.match('/static/offline.html');
                }
            } catch (error) {
                // Comprehensive error handling
                console.error('Service Worker Fetch Error:', error);
                return caches.match('/static/offline.html');
            }
        })()
    );
});