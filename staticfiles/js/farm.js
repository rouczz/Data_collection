// Initialize IndexedDB
async function initDatabase() {
    if (typeof idb === 'undefined') {
        return Promise.reject(new Error("idb library not available"));
    }
    return idb.openDB('farmerApp', 2, {
        upgrade(db) {
            if (!db.objectStoreNames.contains('farmers')) {
                db.createObjectStore('farmers', { keyPath: 'id', autoIncrement: true });
            }
            if (!db.objectStoreNames.contains('farms')) {
                db.createObjectStore('farms', { keyPath: 'id', autoIncrement: true });
            }
        }
    });
}

// Initialize IndexedDB
// async function initDatabase() {
//     return openDB('farmerApp', 1, {
//         upgrade(db) {
//             if (!db.objectStoreNames.contains('farmers')) {
//                 db.createObjectStore('farmers', { keyPath: 'id', autoIncrement: true });
//             }
//             if (!db.objectStoreNames.contains('farms')) {
//                 db.createObjectStore('farms', { keyPath: 'id', autoIncrement: true });
//             }
//         }
//     });
// }

// Initialize IndexedDB


document.addEventListener('DOMContentLoaded', async () => {
    // Extract farmer_id from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const farmerId = urlParams.get('farmer_id');
    if (!farmerId) {
        alert('Farmer ID is missing. Please start from the Farmer page.');
        return;
    }

    // Retrieve farmer details from IndexedDB
    try {
        const db = await initDatabase();
        const tx = db.transaction('farmers', 'readonly');
        const farmer = await tx.store.get(parseInt(farmerId));
        await tx.done;

        if (!farmer) {
            alert('Farmer not found. Please start from the Farmer page.');
            return;
        }

        // Display farmer's name on the page
        const pageTitle = document.getElementById('pageTitle');
        pageTitle.textContent = `Add Farm for ${farmer.first_name} ${farmer.last_name}`;
    } catch (error) {
        console.error('Error retrieving farmer details:', error);
        alert('Failed to load farmer details. Please refresh the page.');
    }
});

document.getElementById('farmForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    // Collect form data
    const formData = new FormData(event.target);
    const farmData = {};
    formData.forEach((value, key) => {
        farmData[key] = value;
    });

    // Extract farmer_id from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const farmerId = urlParams.get('farmer_id');
    if (!farmerId) {
        alert('Farmer ID is missing. Please start from the Farmer page.');
        return;
    }

    // Add metadata
    farmData.farmer_id = parseInt(farmerId);
    farmData.timestamp = new Date().toISOString();
    farmData.synced = false; // Mark as unsynced

    // Save data to IndexedDB
    try {
        const db = await initDatabase();
        const tx = db.transaction('farms', 'readwrite');
        const localId = await tx.store.add(farmData); // Auto-generate ID
        await tx.done;

        alert('Farm data saved offline.');

        // Hide the form and display success message
        document.getElementById('farmForm').style.display = 'none';
        document.getElementById('message').innerHTML = `
            <div class="alert alert-success">
                <p>Farm created successfully!</p>
                <button class="btn btn-primary mt-2" id="addAnotherFarmBtn">Add Another Farm</button>
                <button class="btn btn-success mt-2" onclick="proceedToPlantation(${farmerId})">Proceed to Plantation</button>
            </div>
        `;

        // Attach event listener to the "Add Another Farm" button
        document.getElementById('addAnotherFarmBtn').addEventListener('click', addAnotherFarm);
    } catch (error) {
        console.error('Error saving farm data:', error);
        alert('Failed to save farm data. Please try again.');
    }
});

// Function to add another farm
function addAnotherFarm() {
    // Reset the form
    document.getElementById('farmForm').reset();
    document.getElementById('message').innerHTML = '';
    document.getElementById('farmForm').style.display = 'block';

    // Clear any previously drawn boundaries (if using a map)
    if (window.drawnItems) {
        window.drawnItems.clearLayers();
    }
}

// Function to proceed to plantation
function proceedToPlantation(farmerId) {
    if (!farmerId) {
        alert('Farmer ID is missing. Cannot proceed to plantation.');
        return;
    }
    window.location.href = `/add-plantation/?farmer_id=${farmerId}`;
}