// Initialize IndexedDB
async function initDatabase() {
    return openDB('farmerApp', 1, {
        upgrade(db) {
            if (!db.objectStoreNames.contains('farmers')) {
                db.createObjectStore('farmers', { keyPath: 'id', autoIncrement: true });
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