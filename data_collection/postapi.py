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


import requests
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Farm

def send_farm_data(request, farm_id):
    try:
        # Retrieve the Farm object by ID
        farm = Farm.objects.get(id=farm_id)

        # Convert the PolygonField boundary to GeoJSON format
        # boundary = {
        #     "coordinates": [list(polygon.coords) for polygon in farm.boundary],
        #     "type": "Polygon"
        # }
        boundary = {
            "coordinates": list(farm.boundary.coords),
            "type": "Polygon"
        }

        # Prepare the payload in the required format
        payload = {
            "farmer_id": 145529,
            "farm_name": farm.farm_name,
            "area_in_acres": farm.area_in_acres,
            "ownership": farm.ownership,
            "owner_mobile_number": farm.owner_mobile_number,
            "owner_full_name": farm.owner_full_name,
            "boundary_method": farm.boundary_method,
            "metadata": farm.metadata or {},
            "boundary": boundary
        }

        # Include Authentication Token (JWT) and other headers
        headers = {
            'X-Client-ID': x_client_id,  # Replace with your actual X-Client-ID
            'Authorization': f'Bearer {token}'  # Replace with your actual JWT token
        }

        # Send the POST request to the third-party API
        response = requests.post(
            "https://backend.varahaag.com//api/user/v1/plantation/agfarm/create/",
            json=payload,
            headers=headers
        )

        # Check the response status
        if response.status_code == 201:  # Success
            print(response.json())
            return JsonResponse({"success": True, "message": "Farm data sent successfully!"})
        else:  # Error
            return JsonResponse({"success": False, "error": response.json()}, status=response.status_code)

    except ObjectDoesNotExist:
        return JsonResponse({"error": "Farm not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
import requests
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Plantation

def send_plantation_data(request, plantation_id):
    try:
        # Retrieve the Plantation object by ID
        plantation = Plantation.objects.get(id=plantation_id)

        # Convert the PolygonField boundary to GeoJSON format
        boundary = {
            "coordinates": list(plantation.boundary.coords),
            "type": "Polygon"
        }

        # Prepare the payload in the required format
        payload = {
            "farm_id": 59834,
            "kyari_name": plantation.kyari_name,
            # "number_of_saplings": plantation.number_of_saplings,
            "area_in_acres": plantation.area_in_acres,
            "plantation_model": plantation.plantation_model,
            "year": plantation.year,
            "kyari_type": plantation.kyari_type,
            "metadata": plantation.metadata or {},
            "boundary": boundary
        }

        # Include headers for authentication
        headers = {
            'X-Client-ID': x_client_id,  # Replace with your actual X-Client-ID
            'Authorization': f'Bearer {token}'  # Replace with your actual JWT token
        }
        print(payload)
        # Send the POST request to the third-party API
        response = requests.post(
            "https://backend.varahaag.com/api/user/v1/plantation/agkyari/create/",
            json=payload,
            headers=headers
        )

        # Check the response status
        if response.status_code == 201:  # Success
            print(response.json())
            return JsonResponse({"success": True, "message": "Plantation data sent successfully!"})
        else:  # Error
            return JsonResponse({"success": False, "error": response.json()}, status=response.status_code)

    except ObjectDoesNotExist:
        return JsonResponse({"error": "Plantation not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

import requests
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Specie, Plantation

import requests
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Specie  # Ensure you import your Specie model

def send_specie_data(request, specie_id):
    try:
        # Retrieve the Specie object by ID
        specie = Specie.objects.get(id=specie_id)

        # Prepare the payload in the required format
        payload = {
            
                "kyari": 66089,
                "specie": specie.specie_id,
                "number_of_plants": 10,
                "specie_type": "MAIN",
                "plant_spacing": specie.plant_spacing,
                "spacing_cr": specie.spacing_cr,
                "spacing_cl": specie.spacing_cl,
                "spacing_ct": specie.spacing_ct,
                "spacing_cb": specie.spacing_cb,
                "specie_attributes": {},
                "metadata": {}
            
        }

        # Include headers for authentication
        headers = {
            'X-Client-ID': x_client_id,  # Replace with your actual X-Client-ID
            'Authorization': f'Bearer {token}'  # Replace with your actual JWT token
        }

        # Debugging: Print the payload and headers
        print("Payload:", payload)
        print("Headers:", headers)

        try:
            # Send the POST request to the third-party API
            response = requests.post(
                "https://backend.varahaag.com/api/user/v1/agkyari/specie/create/",
                json=payload,
                headers=headers
            )

            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": f"Request failed: {str(e)}"}, status=500)

        # Debugging: Print the response
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.text)

        try:
            response_json = response.json()
        except ValueError as e:
            return JsonResponse({"error": "Invalid JSON response from server", "response_content": response.text}, status=500)

        # Check the response status
        if response.status_code == 201:  # Success
            return JsonResponse({"success": True, "message": "Species data sent successfully!"})
        else:
            return JsonResponse({"success": False, "error": response_json}, status=response.status_code)

    except ObjectDoesNotExist:
        return JsonResponse({"error": "Species not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)