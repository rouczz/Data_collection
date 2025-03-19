from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import *
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry
from .models import *

def create_farmer(request):
    if request.method == 'POST':

        form = FarmerForm(request.POST, request.FILES)  # ✅ Include request.FILES
        lat = request.POST.get('latitude')
        lng = request.POST.get('longitude')

        if form.is_valid() and lat and lng:
            farmer = form.save(commit=False)
            farmer.block_id = request.POST.get("block_id")  # Save the block_id
            farmer.geo_tag = Point(float(lng), float(lat))
            

            if 'consent_form' in request.FILES:
                farmer.consent_form = request.FILES['consent_form']
                
            farmer.save()  # ✅ Now save the farmer with the file
            print("✅ Farmer Saved Successfully with File!")

            return redirect('add_farm', farmer_id=farmer.id)  # Redirect to farm creation

        else:
            print("❌ Form Errors:", form.errors)  

    else:
        form = FarmerForm()

    return render(request, 'data_collection/templates/create_farmer.html', {'form': form})



def add_farm(request, farmer_id):
    farmer = get_object_or_404(Farmer, id=farmer_id)

    if request.method == "POST":
        form = FarmForm(request.POST)
        boundary_geojson = request.POST.get('boundary')
        if form.is_valid():
            farm = form.save(commit=False)
            farm.farmer = farmer  # ✅ Link farm to the farmer
            farm.boundary = GEOSGeometry(boundary_geojson) 
            farm.save()
            return JsonResponse({"success": True, "farm_id": farm.id})  # ✅ Send farmer_id
        else:
            return JsonResponse({"success": False, "errors": form.errors})

    return render(request, "data_collection/templates/add_farm.html", {"form": FarmForm(), "farmer": farmer})


# def add_plantation(request, farm_id):
#     farm = get_object_or_404(Farm, id=farm_id)

#     if request.method == "POST":
#         form = PlantationForm(request.POST)
#         boundary_geojson = request.POST.get("boundary")

#         if form.is_valid() and boundary_geojson:
#             plantation = form.save(commit=False)
#             plantation.farm = farm
#             plantation.boundary = GEOSGeometry(boundary_geojson)  # ✅ Convert GeoJSON to Polygon
#             plantation.save()
#             return JsonResponse({"success": True, "plantation_id": plantation.id})

#         return JsonResponse({"success": False, "errors": form.errors}, status=400)

#     else:
#         form = PlantationForm()

#     return render(request, "data_collection/templates/add_plantation.html", {"form": form, "farm": farm})
def add_plantation(request, farmer_id):
    farmer = get_object_or_404(Farmer, id=farmer_id)
    farms = Farm.objects.filter(farmer=farmer)
    
    if request.method == "POST":
        print("DEBUG: Request POST Data:", request.POST)
        form = PlantationForm(request.POST)
        farm_id = request.POST.get("farm_id")
        boundary_geojson = request.POST.get("boundary")
        
        if form.is_valid() and boundary_geojson:
            plantation = form.save(commit=False)
            plantation.farmer = farmer
            plantation.farm = get_object_or_404(Farm, id=farm_id)
            
            # Parse the GeoJSON string to extract just the geometry portion
            try:
                import json
                geojson_obj = json.loads(boundary_geojson)
                
                # Extract just the geometry part if it's a Feature
                if geojson_obj.get('type') == 'Feature':
                    geometry_json = json.dumps(geojson_obj['geometry'])
                else:
                    geometry_json = boundary_geojson
                
                # Convert to GEOSGeometry
                plantation.boundary = GEOSGeometry(geometry_json)
                plantation.save()
                return JsonResponse({
                    "success": True,
                    "plantation_id": plantation.id,
                    "farmer_id": farmer_id  # Include the farmer_id in the response
                })
            except Exception as e:
                print(f"ERROR parsing GeoJSON: {str(e)}")
                return JsonResponse({"success": False, "errors": f"Invalid boundary format: {str(e)}"})
        else:
            errors = form.errors
            return JsonResponse({"success": False, "errors": dict(errors)})
    else:
        form = PlantationForm()
    
    return render(request, "data_collection/templates/add_plantation.html", {"form": form, "farms": farms, "farmer": farmer, "farmer_id": farmer.id})


from django.db.models import Q
from django.db.models import Count

from django.db.models import Exists, OuterRef

from django.db.models import Count

def add_specie(request, farmer_id):
    farmer = get_object_or_404(Farmer, id=farmer_id)

    # Annotate the count of related species and filter plantations without species
    plantations = Plantation.objects.filter(
        farm__farmer=farmer
    ).annotate(
        species_count=Count('species')  # Count related species using the related_name 'species'
    ).filter(species_count=0)  # Only include plantations without species

    if request.method == "POST":
        form = SpecieForm(request.POST)
        plantation_id = request.POST.get("plantation_id")

        if form.is_valid() and plantation_id:
            plantation = get_object_or_404(Plantation, id=plantation_id)

            # Save the new species
            specie = form.save(commit=False)
            specie.plantation = plantation
            specie.save()
            return JsonResponse({"success": True, "specie_id": specie.id, "message": "Species added successfully!", "farmer_id": farmer_id })
        else:
            errors = form.errors
            if not plantation_id:
                errors['plantation_id'] = ['Please select a plantation']
            return JsonResponse({"success": False, "errors": errors}, status=400)

    else:
        form = SpecieForm()

    return render(
        request,
        "data_collection/templates/add_specie.html",
        {"form": form, "plantations": plantations, "farmer": farmer, "farmer_id":farmer_id},
    )

def dashboard(request):
    return render(request, "data_collection/templates/dashboard.html") 


from django.shortcuts import render
from django.http import JsonResponse
from .models import Farmer, Farm, Plantation

def get_farmers_list(request):
    search_query = request.GET.get("search", "").strip()  # Get search input
    farmers = Farmer.objects.all()

    if search_query:
        farmers = farmers.filter(first_name__icontains=search_query)  # Case-insensitive search

    farmer_data = [
        {
            "id": farmer.id,
            "name": f"{farmer.first_name} {farmer.last_name}",
            "mobile": farmer.mobile_number,
            "village": farmer.village
        }
        for farmer in farmers
    ]

    return JsonResponse({"farmers": farmer_data})


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Farmer, Farm, Plantation, Specie

def get_farmer_details(request, farmer_id):
    farmer = get_object_or_404(Farmer, id=farmer_id)
    farms = Farm.objects.filter(farmer=farmer)
    plantations = Plantation.objects.filter(farm__in=farms)
    # species = Specie.objects.filter(plantation__in=plantations)
    # ✅ Ensure image URL is absolute (Fixes issue)
    image_url = request.build_absolute_uri(farmer.consent_form.url) if farmer.consent_form else None  
    farmer_data = {
        "id": farmer.id,
        "name": f"{farmer.first_name} {farmer.last_name}",
        "aadhar": farmer.aadhar,
        "mobile": farmer.mobile_number,
        "gender": farmer.gender,
        "guardian": farmer.guardian_name,
        "village": farmer.village,
        "pincode": farmer.pincode,
        "farmer_consent": farmer.farmer_consent,
        "image_url":image_url,
        "geo_tag": {
            "type": "Point",
            "coordinates": [farmer.geo_tag.x, farmer.geo_tag.y]
        }
    }

    farm_data = [
        {
            "id": farm.id,
            "farm_name": farm.farm_name,
            "area": farm.area_in_acres,
            "ownership": farm.ownership,
            "boundary_method": farm.boundary_method,
            "boundary": {
                "type": "Polygon",
                "coordinates": [[list(reversed(coord)) for coord in farm.boundary.coords[0]]] 
            }
        }
        for farm in farms
    ]

    plantation_data = [
        {
            "id": plantation.id,
            "kyari_name": plantation.kyari_name,
            "number_of_saplings": plantation.number_of_saplings,
            "plantation_model": plantation.plantation_model,
            "kyari_type": plantation.kyari_type,
            "is_feasible": plantation.is_feasible,
            "boundary": {
                "type": "Polygon",
                "coordinates": [[list(reversed(coord)) for coord in plantation.boundary.coords[0]]]
            }
        }
        for plantation in plantations
    ]

    # specie_data = [
    #     {
    #         "id": specie.id,
    #         "plantation_id": specie.plantation.id,
    #         "specie_name": specie.specie_name,
    #         "number_of_plants": specie.number_of_plants,
    #         "plant_spacing": specie.plant_spacing
    #     }
    #     for specie in species
    # ]

    return JsonResponse({
        "farmer": farmer_data,
        "farms": farm_data,
        "plantations": plantation_data,
        # "species": specie_data
    })

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.gis.geos import GEOSGeometry
from .models import Farmer, Farm

def get_farms_for_farmer(request, farmer_id):
    """Return a list of farms for the given farmer with valid GeoJSON boundary."""
    farmer = get_object_or_404(Farmer, id=farmer_id)
    farms = Farm.objects.filter(farmer=farmer)

    farm_data = [
        {
            "id": farm.id,
            "farm_name": farm.farm_name,
            "boundary": GEOSGeometry(farm.boundary).geojson  # ✅ Convert to GeoJSON format
        }
        for farm in farms
    ]

    return JsonResponse({"farms": farm_data})

def get_plantations_for_farm(request, farm_id):
    """Return all plantations for the given farm with their GeoJSON boundaries."""
    farm = get_object_or_404(Farm, id=farm_id)
    plantations = Plantation.objects.filter(farm=farm)
    
    plantation_data = [
        {
            "id": plantation.id,
            "kyari_name": plantation.kyari_name,
            "area_in_acres": plantation.area_in_acres,
            "year": plantation.year,
            "kyari_type": plantation.kyari_type,
            "boundary": GEOSGeometry(plantation.boundary).geojson  # Convert to GeoJSON format
        }
        for plantation in plantations
    ]
    
    # Also return the farm boundary for validation
    farm_boundary = GEOSGeometry(farm.boundary).geojson
    
    return JsonResponse({
        "plantations": plantation_data,
        "farm_boundary": farm_boundary
    })

from django.core.files.base import ContentFile
import base64

def upload_media(request, farmer_id):
    farmer = get_object_or_404(Farmer, id=farmer_id)

    if request.method == "POST":
        try:
            # Create a new FarmerMedia instance
            media = FarmerMedia(farmer=farmer)

            # Handle file uploads
            if "picture" in request.FILES:
                media.picture = request.FILES["picture"]
            if "photo_of_english_epic" in request.FILES:
                media.photo_of_english_epic = request.FILES["photo_of_english_epic"]
            if "photo_of_regional_language_epic" in request.FILES:
                media.photo_of_regional_language_epic = request.FILES["photo_of_regional_language_epic"]
            if "id_proof_front" in request.FILES:
                media.id_proof_front = request.FILES["id_proof_front"]
            if "id_proof_back" in request.FILES:
                media.id_proof_back = request.FILES["id_proof_back"]
            if "land_ownership" in request.FILES:
                media.land_ownership = request.FILES["land_ownership"]
            if "picture_of_tree" in request.FILES:
                media.picture_of_tree = request.FILES["picture_of_tree"]

            # Handle digital signature (base64 string from canvas)
            signature_data = request.POST.get("digital_signature")
            if signature_data and ';base64,' in signature_data:
                format, imgstr = signature_data.split(';base64,')
                ext = format.split('/')[-1]
                signature_file = ContentFile(base64.b64decode(imgstr), name=f"signature_{farmer.id}.{ext}")
                media.digital_signature.save(f"signature_{farmer.id}.{ext}", signature_file, save=False)

            # Save the media instance
            media.save()
            
            print("Successfully uploaded farmer media!")
            return JsonResponse({
                "success": True,
                "message": "Farmer media uploaded successfully!",
                "farmer_id": farmer_id
            })
        except Exception as e:
            import traceback
            print(f"Error uploading media: {str(e)}")
            print(traceback.format_exc())
            return JsonResponse({
                "success": False, 
                "errors": str(e)
            }, status=400)
    
    return render(request, "data_collection/templates/farmer_media.html", {"farmer": farmer, "farmer_id": farmer.id})

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# AWS S3 Settings
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
AWS_S3_FILE_OVERWRITE = os.getenv('AWS_S3_FILE_OVERWRITE', False)
AWS_DEFAULT_ACL = os.getenv('AWS_DEFAULT_ACL', None)
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# Use S3 as the default storage backend
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'