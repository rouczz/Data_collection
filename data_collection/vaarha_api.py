from django.http import JsonResponse
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve token and X-Client-ID from environment variables
API_TOKEN = os.getenv("API_TOKEN")
X_CLIENT_ID = os.getenv("X_CLIENT_ID")

# Helper function to make authenticated API calls
def fetch_data_from_external_api(url):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "X-Client-ID": X_CLIENT_ID,
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Fetch States
def get_states(request):
    url = "https://backend.varahaag.com/core/api/state/all/?country_id=2"
    data = fetch_data_from_external_api(url)
    if data:
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"error": "Failed to fetch states"}, status=500)

# Fetch Districts
def get_districts(request, state_id):
    url = f"https://backend.varahaag.com/core/api/district/all/?state_id={state_id}"
    data = fetch_data_from_external_api(url)
    if data:
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"error": "Failed to fetch districts"}, status=500)

# Fetch Blocks
def get_blocks(request, district_id):
    url = f"https://backend.varahaag.com/core/api/block/all/?district_id={district_id}"
    data = fetch_data_from_external_api(url)
    if data:
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"error": "Failed to fetch blocks"}, status=500)
    
def get_species(request):
    url = "https://backend.varahaag.com/core/api/plantation/species/all/"
    data = fetch_data_from_external_api(url)
    if data:
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"error": "Failed to fetch species data"}, status=500)