# import requests
# from django.http import JsonResponse
# from data_collection.models import Farmer
# from django.contrib.gis.geos import GEOSGeometry
# from django.conf import settings

# THIRD_PARTY_API_URL = "https://backend.varahaag.com/api/user/v1/farmer/create/"  # Replace with actual API
# # Extract the token and X-Client-ID from the provided data
# token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoidXNlciIsInR5cGUiOiJhY3RpdmUiLCJ1c2VyX2lkIjozODQ4LCJjb3VudHJ5X2lkIjoyLCJlbWFpbCI6InJvdW5ha0BraXNhbm1pdHJhLmFpIiwib3JnX2NvZGUiOiJLSVM4MTU0IiwiaXNzIjoiaHR0cHM6Ly9iYWNrZW5kLnZhcmFoYWFnLmNvbSIsImlhdCI6MTc0MTI2MTIyOCwiZXhwIjoxNzQ2NDQ1MjI4fQ.RPRBq5jwhBbSBYdKxIdMS0I-FG278DJ2uFZkiU-NSis"
# x_client_id = "partner_app"
# def send_farmer_data(request, farmer_id):
#     try:
#         farmer = Farmer.objects.get(id=farmer_id)
#         print(farmer.country_id)
#         # Convert GIS Point to GeoJSON format
#         geo_tag = {
#             "coordinates": list(farmer.geo_tag.coords),
#             "type": "Point"
#         }

#         # Prepare Data Payload
#         payload = {
#             "aadhar": farmer.aadhar or "",
#             "mobile_number": farmer.mobile_number,
#             "country_id": farmer.country_id,
#             "block_id": farmer.block_id,
#             "village": farmer.village,
#             "pincode": farmer.pincode,
#             "first_name": farmer.first_name,
#             "last_name": farmer.last_name,
#             "gender": farmer.gender,
#             "farmer_consent": farmer.farmer_consent,
#             "geo_tag": geo_tag,
#             "metadata": {"name": "Rounak"}
#         }

#         # **Include Authentication Token (JWT)**
#         headers = {
#             'X-Client-ID': x_client_id,  # Add X-Client-ID header
#             'Authorization': f'Bearer {token}'  # Add Authorization header with the Bearer token
#         }

#         # **Send the POST Request**
#         response = requests.post(THIRD_PARTY_API_URL, json=payload, headers=headers)

#         # **Check Response**
#         if response.status_code == 201:  # ✅ Success
#             print(response.json())
#             return JsonResponse({"success": True, "message": "Farmer data sent successfully!"})
#         else:  # ❌ Error
#             return JsonResponse({"success": False, "error": response.json()}, status=response.status_code)

#     except Farmer.DoesNotExist:
#         return JsonResponse({"error": "Farmer not found"}, status=404)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)


# import requests
# from django.http import JsonResponse
# from django.core.exceptions import ObjectDoesNotExist
# from .models import Farm

# def send_farm_data(request, farm_id):
#     try:
#         # Retrieve the Farm object by ID
#         farm = Farm.objects.get(id=farm_id)

#         # Convert the PolygonField boundary to GeoJSON format
#         # boundary = {
#         #     "coordinates": [list(polygon.coords) for polygon in farm.boundary],
#         #     "type": "Polygon"
#         # }
#         boundary = {
#             "coordinates": list(farm.boundary.coords),
#             "type": "Polygon"
#         }

#         # Prepare the payload in the required format
#         payload = {
#             "farmer_id": 145529,
#             "farm_name": farm.farm_name,
#             "area_in_acres": farm.area_in_acres,
#             "ownership": farm.ownership,
#             "owner_mobile_number": farm.owner_mobile_number,
#             "owner_full_name": farm.owner_full_name,
#             "boundary_method": farm.boundary_method,
#             "metadata": farm.metadata or {},
#             "boundary": boundary
#         }

#         # Include Authentication Token (JWT) and other headers
#         headers = {
#             'X-Client-ID': x_client_id,  # Replace with your actual X-Client-ID
#             'Authorization': f'Bearer {token}'  # Replace with your actual JWT token
#         }

#         # Send the POST request to the third-party API
#         response = requests.post(
#             "https://backend.varahaag.com//api/user/v1/plantation/agfarm/create/",
#             json=payload,
#             headers=headers
#         )

#         # Check the response status
#         if response.status_code == 201:  # Success
#             print(response.json())
#             return JsonResponse({"success": True, "message": "Farm data sent successfully!"})
#         else:  # Error
#             return JsonResponse({"success": False, "error": response.json()}, status=response.status_code)

#     except ObjectDoesNotExist:
#         return JsonResponse({"error": "Farm not found"}, status=404)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)
    
# import requests
# from django.http import JsonResponse
# from django.core.exceptions import ObjectDoesNotExist
# from .models import Plantation

# def send_plantation_data(request, plantation_id):
#     try:
#         # Retrieve the Plantation object by ID
#         plantation = Plantation.objects.get(id=plantation_id)

#         # Convert the PolygonField boundary to GeoJSON format
#         boundary = {
#             "coordinates": list(plantation.boundary.coords),
#             "type": "Polygon"
#         }

#         # Prepare the payload in the required format
#         payload = {
#             "farm_id": 59834,
#             "kyari_name": plantation.kyari_name,
#             # "number_of_saplings": plantation.number_of_saplings,
#             "area_in_acres": plantation.area_in_acres,
#             "plantation_model": plantation.plantation_model,
#             "year": plantation.year,
#             "kyari_type": plantation.kyari_type,
#             "metadata": plantation.metadata or {},
#             "boundary": boundary
#         }

#         # Include headers for authentication
#         headers = {
#             'X-Client-ID': x_client_id,  # Replace with your actual X-Client-ID
#             'Authorization': f'Bearer {token}'  # Replace with your actual JWT token
#         }
#         print(payload)
#         # Send the POST request to the third-party API
#         response = requests.post(
#             "https://backend.varahaag.com/api/user/v1/plantation/agkyari/create/",
#             json=payload,
#             headers=headers
#         )

#         # Check the response status
#         if response.status_code == 201:  # Success
#             print(response.json())
#             return JsonResponse({"success": True, "message": "Plantation data sent successfully!"})
#         else:  # Error
#             return JsonResponse({"success": False, "error": response.json()}, status=response.status_code)

#     except ObjectDoesNotExist:
#         return JsonResponse({"error": "Plantation not found"}, status=404)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)
    

# import requests
# from django.http import JsonResponse
# from django.core.exceptions import ObjectDoesNotExist
# from .models import Specie, Plantation

# import requests
# from django.http import JsonResponse
# from django.core.exceptions import ObjectDoesNotExist
# from .models import Specie  # Ensure you import your Specie model

# def send_specie_data(request, specie_id):
#     try:
#         # Retrieve the Specie object by ID
#         specie = Specie.objects.get(id=specie_id)

#         # Prepare the payload in the required format
#         payload = {
            
#                 "kyari": 66089,
#                 "specie": specie.specie_id,
#                 "number_of_plants": 10,
#                 "specie_type": "MAIN",
#                 "plant_spacing": specie.plant_spacing,
#                 "spacing_cr": specie.spacing_cr,
#                 "spacing_cl": specie.spacing_cl,
#                 "spacing_ct": specie.spacing_ct,
#                 "spacing_cb": specie.spacing_cb,
#                 "specie_attributes": {},
#                 "metadata": {}
            
#         }

#         # Include headers for authentication
#         headers = {
#             'X-Client-ID': x_client_id,  # Replace with your actual X-Client-ID
#             'Authorization': f'Bearer {token}'  # Replace with your actual JWT token
#         }

#         # Debugging: Print the payload and headers
#         print("Payload:", payload)
#         print("Headers:", headers)

#         try:
#             # Send the POST request to the third-party API
#             response = requests.post(
#                 "https://backend.varahaag.com/api/user/v1/agkyari/specie/create/",
#                 json=payload,
#                 headers=headers
#             )

#             response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
#         except requests.exceptions.RequestException as e:
#             return JsonResponse({"error": f"Request failed: {str(e)}"}, status=500)

#         # Debugging: Print the response
#         print("Response Status Code:", response.status_code)
#         print("Response Content:", response.text)

#         try:
#             response_json = response.json()
#         except ValueError as e:
#             return JsonResponse({"error": "Invalid JSON response from server", "response_content": response.text}, status=500)

#         # Check the response status
#         if response.status_code == 201:  # Success
#             return JsonResponse({"success": True, "message": "Species data sent successfully!"})
#         else:
#             return JsonResponse({"success": False, "error": response_json}, status=response.status_code)

#     except ObjectDoesNotExist:
#         return JsonResponse({"error": "Species not found"}, status=404)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)

import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import Farmer, Farm, Plantation, Specie, FarmerMedia

# ✅ Dashboard View (Loads HTML Page)
def dashboard_2(request):
    return render(request, "data_collection/templates/dashboard_2.html")

# ✅ API: Get Sync Status for Farmers
def get_sync_status(request):
    farmers = Farmer.objects.all()
    farmer_data = []

    for farmer in farmers:
        farms = Farm.objects.filter(farmer=farmer)
        plantations = Plantation.objects.filter(farm__in=farms)
        species = Specie.objects.filter(plantation__in=plantations)
        # media = FarmerMedia.objects.filter(ref_id=farmer.id, ref_type="Farmer")

        is_synced = all([
            farmer.vaarha_id,
            all(farm.vaarha_id for farm in farms),
            all(plantation.vaarha_id for plantation in plantations),
            all(specie.vaarha_id for specie in species),
            # all(media.vaarha_id for media in media),
        ])

        farmer_data.append({
            "id": farmer.id,
            "name": f"{farmer.first_name} {farmer.last_name}",
            "mobile": farmer.mobile_number,
            "synced": is_synced,
        })

    synced_farmers = [f for f in farmer_data if f["synced"]]
    pending_farmers = [f for f in farmer_data if not f["synced"]]

    return JsonResponse({"synced": synced_farmers, "pending": pending_farmers})

import json
import requests
from django.http import JsonResponse
from django.conf import settings
from .models import Farmer, Farm, Plantation, Specie, FarmerMedia
import os
from django.views.decorators.csrf import csrf_exempt

from dotenv import load_dotenv

load_dotenv()

VAARHA_API_BASE_URL = "https://backend.varahaag.com/api/user/v1"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('token')}",  # Store API token in settings
    "X-Client-ID": os.getenv('x_client_id'),
}


import json
from django.http import JsonResponse

def push_all_data_to_vaarha(request):
    if request.method == "POST":
        data = json.loads(request.body)
        farmers = data.get("farmers", [])

        errors = []  # ✅ Store any errors

        for farmer_data in farmers:
            farmer = Farmer.objects.get(id=farmer_data["id"])

            # Push Farmer (if not synced)
            if not farmer.vaarha_id:
                response = push_farmers_to_vaarha(farmer)
                if response.status_code != 201:
                    errors.append({"farmer_id": farmer.id, "error": response.json()})

            # Push Farms
            farms = Farm.objects.filter(farmer=farmer)
            for farm in farms:
                if not farm.vaarha_id:
                    response = push_farms_to_vaarha(farm)
                    if response.status_code != 201:
                        errors.append({"farm_id": farm.id, "error": response.json()})

                # Push Plantations
                plantations = Plantation.objects.filter(farm=farm)
                for plantation in plantations:
                    if not plantation.vaarha_id:
                        response = push_plantations_to_vaarha(plantation)
                        if response.status_code != 201:
                            errors.append({"plantation_id": plantation.id, "error": response.json()})

                    # Push Species
                    species = Specie.objects.filter(plantation=plantation)
                    for specie in species:
                        if not specie.vaarha_id:
                            response = push_species_to_vaarha(specie)
                            if response.status_code != 201:
                                errors.append({"specie_id": specie.id, "error": response.json()})

        # ✅ Return success if no errors, else return error messages
        if errors:
            return JsonResponse({"success": False, "errors": errors}, status=400)
        return JsonResponse({"success": True, "message": "All data pushed successfully!"})



# ✅ 1️⃣ Push Farmer to Vaarha
def push_farmers_to_vaarha(farmer):
    farmer_payload = {
        "aadhar": farmer.aadhar if hasattr(farmer, "aadhar") else None,
        "mobile_number": farmer.mobile_number,
        "country_id": 2,
        "block_id": farmer.block_id,
        "village": farmer.village,
        "pincode": farmer.pincode,
        "first_name": farmer.first_name,
        "last_name": farmer.last_name,
        "gender": farmer.gender,
        "farmer_consent": True,
        "geo_tag": {
            "coordinates": [farmer.geo_tag.x, farmer.geo_tag.y],
            "type": "Point"
        }
    }
    response = requests.post(f"{VAARHA_API_BASE_URL}/farmer/create/", json=farmer_payload, headers=HEADERS)
    if response.status_code == 201:
        farmer_data = response.json()
        farmer.vaarha_id = farmer_data["id"]
        farmer.save()

    return response


# ✅ 2️⃣ Push Farm to Vaarha
def push_farms_to_vaarha(farm):
    farm_payload = {
        "farmer_id": farm.farmer.vaarha_id,
        "farm_name": farm.farm_name,
        "area_in_acres": farm.area_in_acres,
        "ownership": farm.ownership,
        "boundary_method": farm.boundary_method,
        "boundary": {
            "coordinates": [list(farm.boundary.coords[0])],
            "type": "Polygon"
        },
        "metadata": {}
    }
    response = requests.post(f"{VAARHA_API_BASE_URL}/plantation/agfarm/create/", json=farm_payload, headers=HEADERS)
    if response.status_code == 201:
        farm_data = response.json()
        farm.vaarha_id = farm_data["id"]
        farm.save()

    return response


# ✅ 3️⃣ Push Plantation (Kyari) to Vaarha
def push_plantations_to_vaarha(plantation):
    plantation_payload = {
        "farm_id": plantation.farm.vaarha_id,
        "kyari_name": plantation.kyari_name,
        "area_in_acres": plantation.area_in_acres,
        "number_of_saplings": plantation.number_of_saplings,
        "plantation_model": plantation.plantation_model,
        "year": plantation.year,
        "kyari_type": plantation.kyari_type,
        "boundary": {
            "coordinates": [list(plantation.boundary.coords[0])],
            "type": "Polygon"
        }
    }
    response = requests.post(f"{VAARHA_API_BASE_URL}/plantation/agkyari/create/", json=plantation_payload, headers=HEADERS)
    if response.status_code == 201:
        plantation_data = response.json()
        plantation.vaarha_id = plantation_data["id"]
        plantation.save()

    return response


# ✅ 4️⃣ Push Specie to Vaarha
def push_species_to_vaarha(specie):
    specie_payload = {
        "kyari": specie.plantation.vaarha_id,
        "specie": specie.specie_id,
        "specie_type": "MAIN", 
        "number_of_plants": specie.number_of_plants, 
             
        "plant_spacing": specie.plant_spacing,
        "spacing_cr": specie.spacing_cr,
        "spacing_cl": specie.spacing_cl,
        "spacing_ct": specie.spacing_ct,
        "spacing_cb": specie.spacing_cb,
        "specie_attributes": {},
        "metadata": {}
    }
    response = requests.post(f"{VAARHA_API_BASE_URL}/agkyari/specie/create/", json=specie_payload, headers=HEADERS)
    if response.status_code == 201:
        specie_data = response.json()
        specie.vaarha_id = specie_data["id"]
        specie.save()
    return response


# ✅ 5️⃣ Push Media to Vaarha (Upload Flow)
# def push_media_to_vaarha(ref_id, ref_type):
#     media_files = FarmerMedia.objects.filter(ref_id=ref_id, ref_type=ref_type, vaarha_id__isnull=True)

#     for media in media_files:
#         # First, request upload URL
#         media_payload = {
#             "ref_type": ref_type,
#             "ref_id": ref_id,
#             "farmer_id": ref_id if ref_type == "Farmer" else None,
#             "content_length": media.file.size
#         }
#         response = requests.post(f"{VAARHA_API_BASE_URL}/farmer/media/upload/", json=media_payload, headers=HEADERS)

#         if response.status_code == 201:
#             upload_data = response.json()
#             upload_url = upload_data["media_details"]["s3_data"]["url"]
#             upload_fields = upload_data["media_details"]["s3_data"]["fields"]

#             # Now, upload the actual file to S3
#             with open(media.file.path, 'rb') as f:
#                 files = {"file": f}
#                 upload_s3_response = requests.post(upload_url, data=upload_fields, files=files)

#             if upload_s3_response.status_code == 204:
#                 media.vaarha_id = upload_data["id"]
#                 media.save()
#             else:
#                 print("❌ Failed to upload media:", upload_s3_response.text)
