const CACHE_NAME = "kisanmitra-cache-v4";
const urlsToCache = [
  "/",
  "/create_farmer/",
  "/add_farm/:farmer_id/",
  "/api/farms/:farmer_id/",
  "/add-plantation/:farmer_id/",
  "/add-species/:farmer_id/",
  "/dashboard-data/:farmer_id/",
  "/dashboard-farmers/",
  "/dashboard/",
  "/get-plantations/:farm_id/",
  "/upload-media/:farmer_id/",
  "/static/css/style.css",
  "/static/js/app.js",
  "/static/icons/image.png",
  "/static/icons/image copy.png",
  "/offline.html",
  '/static/css/bootstrap.min.css',
  '/static/js/bootstrap.bundle.min.js',
  'https://unpkg.com/leaflet@1.9.3/dist/leaflet.css',
  'https://unpkg.com/leaflet@1.9.3/dist/leaflet.js',
  'https://cdnjs.cloudflare.com/ajax/libs/idb/7.1.1/idb.min.js',

];

// Install Event: Cache Static Assets
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(urlsToCache);
    })
  );
});

// Fetch Event: Serve Cached Resources or Fetch from Network
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      // If the resource is in the cache, return it
      if (response) {
        return response;
      }

      // Otherwise, fetch the resource from the network
      return fetch(event.request).catch(() => {
        // If the request fails and the resource is not cached, serve the offline page
        if (event.request.mode === "navigate" || event.request.destination === "document") {
          return caches.match("/offline.html");
        }
      });
    })
  );
});

// Activate Event: Clear Old Caches
self.addEventListener("activate", (event) => {
  const cacheWhitelist = [CACHE_NAME];

  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (!cacheWhitelist.includes(cacheName)) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});