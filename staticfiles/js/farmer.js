// // Initialize IndexedDB

// function initializeDataFunctions() {
//     // First try to load the library
//     loadIdbLibrary()
//         .then(() => {
//             console.log("idb library loaded successfully");
//             return initDatabase();
//         })
//         .then((db) => {
//             console.log("Database initialized successfully");
//             return Promise.all([
//                 fetchAndCacheHierarchyData(db),
//                 populateDropdownsFromCache(db)
//             ]);
//         })
//         .then(() => {
//             console.log("Data loaded and dropdowns populated");
//             setupEventListeners();
//         })
//         .catch(error => {
//             console.error("Error during initialization:", error);
//             const errorMessage = document.createElement("div");
//             errorMessage.style.color = "red";
//             errorMessage.style.padding = "10px";
//             errorMessage.textContent = "Unable to initialize offline capabilities. Please check your internet connection and refresh the page.";
//             document.body.prepend(errorMessage);
//         });
// }

// Function to load the idb library
// function loadIdbLibrary() {
//     return new Promise((resolve, reject) => {
//         // Check if already loaded
//         if (typeof idb !== 'undefined') {
//             resolve();
//             return;
//         }
        
//         console.log("Loading idb library...");
        
//         // Try to load from multiple CDNs for better reliability

        
//         function tryNextCdn(index) {
//             if (index >= cdnUrls.length) {
//                 reject(new Error("Failed to load idb library from all sources"));
//                 return;
//             }
            
//             const script = document.createElement("script");
//             script.src = cdnUrls[index];
            
//             script.onload = function() {
//                 // Verify the library is actually available
//                 if (typeof idb !== 'undefined') {
//                     resolve();
//                 } else {
//                     console.warn(`idb loaded from ${cdnUrls[index]} but not available in global scope`);
//                     tryNextCdn(index + 1);
//                 }
//             };
            
//             script.onerror = function() {
//                 console.warn(`Failed to load idb from ${cdnUrls[index]}, trying next source`);
//                 tryNextCdn(index + 1);
//             };
            
//             document.head.appendChild(script);
//         }
        
//         // Start with the first CDN
//         tryNextCdn(0);
//     });
// }

// // Initialize the IndexedDB database
// function initDatabase() {
//     if (typeof idb === 'undefined') {
//         return Promise.reject(new Error("idb library not available"));
//     }
    
//     return idb.openDB('farmerApp', 1, {
//         upgrade(db) {
//             // Create stores for our hierarchical data
//             if (!db.objectStoreNames.contains('states')) {
//                 db.createObjectStore('states', { keyPath: 'id' });
//             }
            
//             if (!db.objectStoreNames.contains('districts')) {
//                 db.createObjectStore('districts', { keyPath: 'id' });
//             }
            
//             if (!db.objectStoreNames.contains('blocks')) {
//                 db.createObjectStore('blocks', { keyPath: 'id' });
//             }
            
//             // Store for offline submissions
//             if (!db.objectStoreNames.contains('offlineFarmers')) {
//                 const farmerStore = db.createObjectStore('offlineFarmers', { 
//                     keyPath: 'id',
//                     autoIncrement: true 
//                 });
//                 farmerStore.createIndex('timestamp', 'timestamp');
//             }
            
//             // Store for created farmers (will have server-assigned IDs)
//             if (!db.objectStoreNames.contains('farmers')) {
//                 db.createObjectStore('farmers', { keyPath: 'id' });
//             }
            
//             // Store for farms
//             if (!db.objectStoreNames.contains('farms')) {
//                 const farmStore = db.createObjectStore('farms', { 
//                     keyPath: 'id', 
//                     autoIncrement: true 
//                 });
//                 farmStore.createIndex('farmerId', 'farmer_id');
//             }
//         }
//     });
// }
async function initDatabase() {
    if (typeof idb === 'undefined') {
        return Promise.reject(new Error("idb library not available"));
    }
    return idb.openDB('farmerApp', 1, {
        upgrade(db) {
            if (!db.objectStoreNames.contains('farmers')) {
                db.createObjectStore('farmers', { keyPath: 'id', autoIncrement: true });
            }
            if (!db.objectStoreNames.contains('farmers')) {
                db.createObjectStore('farmers', { keyPath: 'id', autoIncrement: true });
            }
            if (!db.objectStoreNames.contains('farms')) {
                db.createObjectStore('farms', { keyPath: 'id', autoIncrement: true });
            }
        }
    });
}

// Handle form submission
document.getElementById('farmerForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    // Collect form data
    const formData = new FormData(event.target);
    const farmerData = {};
    formData.forEach((value, key) => {
        farmerData[key] = value;
    });

    // Add metadata
    farmerData.timestamp = new Date().toISOString();
    farmerData.synced = false; // Mark as unsynced

    // Save data to IndexedDB
    try {
        const db = await initDatabase();
        const tx = db.transaction('farmers', 'readwrite');
        const localId = await tx.store.add(farmerData); // Auto-generate ID
        await tx.done;

        alert('Farmer data saved offline.');

        // Redirect to the next page with the farmer's local ID
        window.location.href = `/add-farm/?farmer_id=${localId}`;
    } catch (error) {
        console.error('Error saving farmer data:', error);
        alert('Failed to save farmer data. Please try again.');
    }
});