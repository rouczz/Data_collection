import requests
from django.http import JsonResponse
from data_collection.models import Farmer
from django.contrib.gis.geos import GEOSGeometry
from django.conf import settings

THIRD_PARTY_API_URL = "https://backend.varahaag.com/api/user/v1/farmer/create/"  # Replace with actual API
# Extract the token and X-Client-ID from the provided data
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoidXNlciIsInR5cGUiOiJhY3RpdmUiLCJ1c2VyX2lkIjozODQ4LCJjb3VudHJ5X2lkIjoyLCJlbWFpbCI6InJvdW5ha0BraXNhbm1pdHJhLmFpIiwib3JnX2NvZGUiOiJLSVM4MTU0IiwiaXNzIjoiaHR0cHM6Ly9iYWNrZW5kLnZhcmFoYWFnLmNvbSIsImlhdCI6MTc0MTI2MTIyOCwiZXhwIjoxNzQ2NDQ1MjI4fQ.RPRBq5jwhBbSBYdKxIdMS0I-FG278DJ2uFZkiU-NSis"
x_client_id = "partner_app"
def send_farmer_data(request, farmer_id):
    try:
        farmer = Farmer.objects.get(id=farmer_id)
        print(farmer.country_id)
        # Convert GIS Point to GeoJSON format
        geo_tag = {
            "coordinates": list(farmer.geo_tag.coords),
            "type": "Point"
        }

        # Prepare Data Payload
        payload = {
            "aadhar": farmer.aadhar or "",
            "mobile_number": farmer.mobile_number,
            "country_id": farmer.country_id,
            "block_id": farmer.block_id,
            "village": farmer.village,
            "pincode": farmer.pincode,
            "first_name": farmer.first_name,
            "last_name": farmer.last_name,
            "gender": farmer.gender,
            "farmer_consent": farmer.farmer_consent,
            "geo_tag": geo_tag,
            "metadata": {"name": "Rounak"}
        }

        # **Include Authentication Token (JWT)**
        headers = {
            'X-Client-ID': x_client_id,  # Add X-Client-ID header
            'Authorization': f'Bearer {token}'  # Add Authorization header with the Bearer token
        }

        # **Send the POST Request**
        response = requests.post(THIRD_PARTY_API_URL, json=payload, headers=headers)

        # **Check Response**
        if response.status_code == 201:  # ✅ Success
            print(response.json())
            return JsonResponse({"success": True, "message": "Farmer data sent successfully!"})
        else:  # ❌ Error
            return JsonResponse({"success": False, "error": response.json()}, status=response.status_code)

    except Farmer.DoesNotExist:
        return JsonResponse({"error": "Farmer not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


