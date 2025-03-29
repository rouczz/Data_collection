const CACHE_NAME = "kisanmitra-cache-v4";
const urlsToCache = [
  "/",
  "/static/icons/image.png",        // 192x192 icon
  "/static/icons/image%20copy.png", // 512x512 icon (note encoded space)
  
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