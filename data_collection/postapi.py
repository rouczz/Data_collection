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
        media = FarmerMedia.objects.filter(farmer=farmer)

        is_synced = all([
            farmer.vaarha_id,
            all(farm.vaarha_id for farm in farms),
            all(plantation.vaarha_id for plantation in plantations),
            all(specie.vaarha_id for specie in species),
            all(media.vaarha_id for media in media),
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
            media = FarmerMedia.objects.filter(farmer=farmer).first()

            # Push Farmer (if not synced)
            if not farmer.vaarha_id:
                response = push_farmers_to_vaarha(farmer)
                if response.status_code != 201:
                    errors.append({"farmer_id": farmer.id, "error": response.json()})

            # if not media.vaarha_document_id:
            #     response = push_documents_to_vaarha(farmer)
            #     if response.status_code != 201:
            #         errors.append({"farmer_id": farmer.id, "document_error": response.json()})

            # if not media.vaarha_id:
            #     response = push_media_to_vaarha(farmer)
            #     # if response.status_code != 201:
            #     #     errors.append({"farmer_id": farmer.id, "media_error": response.json()})

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

VAARHA_MEDIA_UPLOAD_URL = f"{VAARHA_API_BASE_URL}/api/user/v1/farmer/media/upload/"
# Mapping model fields to Varaha API ref_type & sub_ref_name
MEDIA_MAPPING = {
    "picture": ("Farmer", "ProfilePicture"),
    "photo_of_english_epic": ("Farmer", "RegenFPIC"),
    "photo_of_regional_language_epic": ("Farmer", "RegenFPICLocal"),
    "id_proof": ("Farmer", "IdentityImage"),
    "land_ownership": ("Farm", "LandRecord"),
    "digital_signature": ("Farmer", "ConsentSignature"),
    "centre_top": ("AgroFarmSpecie", "CentreTop"),
    "centre_bottom": ("AgroFarmSpecie", "CentreBottom"),
    "centre_left": ("AgroFarmSpecie", "CentreLeft"),
    "centre_right": ("AgroFarmSpecie", "CentreRight"),
}
def push_media_to_vaarha(farmer):
    media_objects = FarmerMedia.objects.filter(farmer=farmer)
    print("mediaobjects:", media_objects)
    results = []
    
    for media in media_objects:
        for field_name, (ref_type, sub_ref_name) in MEDIA_MAPPING.items():
            file_field = getattr(media, field_name, None)
            if file_field and file_field.name:  # Check if file exists
                try:
                    # Get file size
                    content_length = file_field.size
                    
                    payload = {
                        "ref_type": ref_type,
                        "ref_sub_type": sub_ref_name,
                        "ref_id": farmer.vaarha_id,
                        "farmer_id": farmer.vaarha_id,
                        "content_length": content_length,
                        # "metadata": {"farmer_name": farmer.first_name}
                    }
                    
                    # Send request to get signed S3 URL from Varaha
                    response = requests.post(VAARHA_MEDIA_UPLOAD_URL, json=payload, headers=HEADERS)
                    
                    if response.status_code in [200, 201]:
                        upload_data = response.json().get("media_details", {}).get("s3_data", {})
                        
                        # Read the file content
                        file_field.open('rb')  # Make sure file is open
                        file_content = file_field.read()
                        file_field.close()
                        
                        # Get filename from the path
                        filename = file_field.name.split('/')[-1]
                        
                        # Perform upload to Varaha's S3 using the signed URL
                        files = {
                            "file": (filename, file_content, upload_data["fields"].get("Content-Type", "application/octet-stream"))
                        }
                        
                        # Add all required fields from the presigned URL
                        s3_response = requests.post(
                            upload_data["url"], 
                            data=upload_data["fields"], 
                            files=files
                        )
                        print("s3_response :",s3_response)
                        # Check for successful upload (S3 can return different success codes)
                        if s3_response.status_code in [200, 201, 204]:
                            # Store response data in vaarha_doc_metadata field
                            media.vaarha_doc_metadata = {
                                "varaha_media_id": response.json().get("id"),
                                "ref_type": ref_type,
                                "sub_ref_name": sub_ref_name,
                                "file_name": file_field.name,
                            }
                            media.save()
                            results.append({
                                "status": "success",
                                "field": field_name,
                                "farmer_id": farmer.id,
                                "media_id": response.json().get("id")
                            })
                        else:
                            results.append({
                                "status": "error",
                                "field": field_name,
                                "farmer_id": farmer.id,
                                "message": f"Failed to upload to S3: {s3_response.status_code} - {s3_response.text}"
                            })
                    else:
                        results.append({
                            "status": "error",
                            "field": field_name,
                            "farmer_id": farmer.id,
                            "message": f"Failed to get S3 URL: {response.status_code} - {response.text}"
                        })
                except Exception as e:
                    results.append({
                        "status": "error",
                        "field": field_name,
                        "farmer_id": farmer.id,
                        "message": f"Exception: {str(e)}"
                    })
    
    return {"message": "Media upload process completed", "results": results}
def push_documents_to_vaarha(farmer):
    media = FarmerMedia.objects.filter(farmer=farmer).first()

    if not media:
        return JsonResponse({"error": "No document available for farmer"}, status=400)

    if media.vaarha_document_id:
        return JsonResponse({"message": "Document already synced"}, status=200)

    document_payload = {
        "doc_type": "IDENTITY_CARD",
        "farmer_id": media.farmer.vaarha_id,
        "doc_reference": media.id_type,
        "document_number": media.id_number,
        "document_details": {
            "type": dict(FarmerMedia.ID_TYPE_CHOICES).get(media.id_type, ""),
            "expiry": media.id_expiry_date.strftime("%Y-%m-%d") if media.id_expiry_date else None
        },
    }
    print("doc_payload:",document_payload)
    response = requests.post(f"{VAARHA_API_BASE_URL}/farmer-document/create/", json=document_payload, headers=HEADERS)
    print("Response", response.json())
    if response.status_code == 201:
        response_data = response.json()
        media.vaarha_document_id = response_data.get("id")
        # Store metadata in vaarha_doc_metadata field
        media.vaarha_doc_metadata = {
            "is_verified": response_data.get("is_verified", False),
            "validated_datetime": response_data.get("validated_datetime"),
            "created_datetime": response_data.get("created_datetime"),
        }
        media.save()
        print("Document data synced successfully:", response_data)

    return response

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
        print("Farmer Data:",farmer_data)
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
    if farm.owner_mobile_number:
        farm_payload["owner_mobile_number"] = farm.owner_mobile_number

    if farm.owner_full_name:
        farm_payload["owner_full_name"] = farm.owner_full_name

    print(farm_payload)
    response = requests.post(f"{VAARHA_API_BASE_URL}/plantation/agfarm/create/", json=farm_payload, headers=HEADERS)
    if response.status_code == 201:
        
        farm_data = response.json()
        print("Farm data:",farm_data)
        farm.vaarha_id = farm_data["id"]
        farm.save()

        # ✅ Upload Landlord Declaration if it exists
        if farm.landlord_declaration:
            print("farm.landlord_declaration",farm.landlord_declaration)
            upload_landlord_declaration(farm)


    return response

import requests
import boto3


# AWS S3 Setup
S3_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
s3_client = boto3.client("s3")

def get_s3_file_details(file_url):
    """Fetch content length & file object from S3."""
    try:
        print("Original File URL:", file_url)  # ✅ Debugging step

        # Extract only the key from the URL
        file_key = file_url.split("farm_landlord_declarations/")[-1]
        file_key = "farm_landlord_declarations/" + file_key  # Ensure full path
        print("Extracted File Key:", file_key)  # ✅ Debugging step

        # Fetch file metadata
        response = s3_client.head_object(Bucket=S3_BUCKET_NAME, Key=file_key)
        content_length = response["ContentLength"]
        return file_key, content_length

    except Exception as e:
        print("Error fetching S3 file details:", e)
        return None, None



def upload_landlord_declaration(farm):
    """Upload the landlord declaration form to Varaha"""
    if not farm.landlord_declaration:
        return None  # No file to upload

    # Get file details from S3
    file_url = farm.landlord_declaration.url
    print("Landlord Declaration URL:", farm.landlord_declaration.url)

    file_key, content_length = get_s3_file_details(file_url)

    if not file_key or not content_length:
        return None  # Failed to fetch S3 file details

    # Step 1: Get upload URL from Varaha
    payload = {
        "ref_type": "Farm",
        "ref_sub_type": "LandLordDeclaration",
        "ref_id": farm.farmer.vaarha_id,  # The farmer ID in Varaha
        "farmer_id": farm.farmer.vaarha_id,  # The farmer's ID in Varaha
        "content_length": content_length
    }

    response = requests.post(f"{VAARHA_API_BASE_URL}/media/request-upload/", json=payload, headers=HEADERS)
    print("Response:", response.json())
    if response.status_code != 201:
        print("Failed to get Varaha upload URL:", response.json())
        return None

    upload_data = response.json()

    upload_url = upload_data["media_details"]["s3_data"]["url"]
    data_fields=upload_data["media_details"]["s3_data"]["fields"]
    if not upload_url:
        print("No upload URL returned from Varaha.")
        return None

    # Step 2: Upload the file to Varaha
    s3_file = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=file_key)["Body"].read()
    
    upload_response = requests.post(upload_url, data=s3_file, fields=data_fields)

    if upload_response.status_code not in [200, 201, 204]:
        print("File upload failed:", upload_response.text)
        return None

    print(f"Successfully uploaded landlord declaration for farm {farm.id}")
    return True



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
        print("Plantation data:", plantation_data)
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
        print("specie resposne",specie_data)
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
