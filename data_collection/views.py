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
            

            # return redirect('add_farm', farmer_id=farmer.id)  # Redirect to farm creation

            return JsonResponse({"success": True,  "farmer_id":farmer.id})  # ✅ Send farmer_id
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
    
    farmer_data = {
        "id": farmer.id,
        "name": f"{farmer.first_name} {farmer.last_name}",
        "mobile": farmer.mobile_number,
        "gender": farmer.gender,
        "guardian": farmer.guardian_name,
        "village": farmer.village,
        "pincode": farmer.pincode,
        "farmer_consent": farmer.farmer_consent,
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

# from django.core.files.base import ContentFile
# import base64

# def upload_media(request, farmer_id):
#     farmer = get_object_or_404(Farmer, id=farmer_id)

#     if request.method == "POST":
#         try:
#             # Create a new FarmerMedia instance
#             media = FarmerMedia(farmer=farmer)

#             # Handle file uploads
#             if "picture" in request.FILES:
#                 media.picture = request.FILES["picture"]
#             if "photo_of_english_epic" in request.FILES:
#                 media.photo_of_english_epic = request.FILES["photo_of_english_epic"]
#             if "photo_of_regional_language_epic" in request.FILES:
#                 media.photo_of_regional_language_epic = request.FILES["photo_of_regional_language_epic"]
#             if "id_proof_front" in request.FILES:
#                 media.id_proof_front = request.FILES["id_proof_front"]
#             if "id_proof_back" in request.FILES:
#                 media.id_proof_back = request.FILES["id_proof_back"]
#             if "land_ownership" in request.FILES:
#                 media.land_ownership = request.FILES["land_ownership"]
#             if "picture_of_tree" in request.FILES:
#                 media.picture_of_tree = request.FILES["picture_of_tree"]

#             # Handle digital signature (base64 string from canvas)
#             signature_data = request.POST.get("digital_signature")
#             if signature_data and ';base64,' in signature_data:
#                 format, imgstr = signature_data.split(';base64,')
#                 ext = format.split('/')[-1]
#                 signature_file = ContentFile(base64.b64decode(imgstr), name=f"signature_{farmer.id}.{ext}")
#                 media.digital_signature.save(f"signature_{farmer.id}.{ext}", signature_file, save=False)

#             # Save the media instance
#             media.save()
            
#             print("Successfully uploaded farmer media!")
#             return JsonResponse({
#                 "success": True,
#                 "message": "Farmer media uploaded successfully!",
#                 "farmer_id": farmer_id
#             })
#         except Exception as e:
#             import traceback
#             print(f"Error uploading media: {str(e)}")
#             print(traceback.format_exc())
#             return JsonResponse({
#                 "success": False, 
#                 "errors": str(e)
#             }, status=400)
    
#     return render(request, "data_collection/templates/farmer_media.html", {"farmer": farmer, "farmer_id": farmer.id})



from django.http import JsonResponse
from django.core.files.base import ContentFile
import base64
from PIL import Image
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import FarmerMedia
from io import BytesIO
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
from io import BytesIO
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
import os
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

def optimize_image(image_file, max_size=(1200, 1200), quality=85):
    """
    Resizes and optimizes an image to reduce file size.
    Returns a BytesIO object containing the optimized image.
    """
    # Open the image
    img = Image.open(image_file)
    
    # Convert image to RGB if it's not (handles RGBA and other formats)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize the image while maintaining aspect ratio
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    # Create a BytesIO object to store the optimized image
    optimized = BytesIO()
    
    # Save the image with reduced quality
    img.save(optimized, format='JPEG', quality=quality, optimize=True)
    
    # Reset the buffer position
    optimized.seek(0)
    
    return optimized

def generate_pdf_from_image(image):
    """
    Creates a PDF from a single image.
    Returns a BytesIO object containing the PDF data.
    """
    # Create a BytesIO buffer to store the PDF
    pdf_buffer = BytesIO()

    # Create a PDF canvas
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter  # Width and height of the PDF page
    
    try:
        # Optimize the image first
        optimized_image = optimize_image(image)
        
        # Open the optimized image
        img = Image.open(optimized_image)
        img_width, img_height = img.size
        aspect_ratio = img_height / img_width

        # Calculate new dimensions while maintaining aspect ratio
        max_width = width * 0.9
        max_height = height * 0.9
        
        new_width = min(max_width, img_width)
        new_height = new_width * aspect_ratio

        if new_height > max_height:
            new_height = max_height
            new_width = new_height / aspect_ratio

        # Save the image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_filename = temp_file.name
            img.save(temp_filename, format="JPEG", quality=85)

        # Draw the image onto the PDF using the temporary file path
        c.drawImage(
            temp_filename,
            30, height - 30 - new_height,
            width=new_width,
            height=new_height
        )
        
        # Delete the temporary file after drawing
        os.unlink(temp_filename)
        
    except Exception as e:
        # Log the error for debugging
        import logging
        logging.error(f"Error processing image: {str(e)}")
        raise

    # Save the PDF
    c.save()

    # Move the buffer pointer to the beginning
    pdf_buffer.seek(0)
    return pdf_buffer

def generate_pdf_from_images(front_image, back_image):
    """
    Combines two images (front and back) into a single PDF file.
    Returns a BytesIO object containing the PDF data.
    Handles both InMemoryUploadedFile and TemporaryUploadedFile.
    """
    # Create a BytesIO buffer to store the PDF
    pdf_buffer = BytesIO()

    # Create a PDF canvas
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter  # Width and height of the PDF page

    # Helper function to add an image to the PDF
    def add_image_to_pdf(image, x, y, max_width, max_height):
        try:
            # Optimize the image first
            optimized_image = optimize_image(image)
            
            # Open the optimized image
            img = Image.open(optimized_image)
            img_width, img_height = img.size
            aspect_ratio = img_height / img_width

            # Calculate new dimensions while maintaining aspect ratio
            new_width = min(max_width, img_width)
            new_height = new_width * aspect_ratio

            if new_height > max_height:
                new_height = max_height
                new_width = new_height / aspect_ratio

            # Save the image to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                temp_filename = temp_file.name
                img.save(temp_filename, format="JPEG", quality=85)

            # Draw the image onto the PDF using the temporary file path
            c.drawImage(
                temp_filename,
                x, y - new_height,
                width=new_width,
                height=new_height
            )
            
            # Delete the temporary file after drawing
            os.unlink(temp_filename)
            
        except Exception as e:
            # Log the error for debugging
            import logging
            logging.error(f"Error processing image: {str(e)}")
            raise

    # Add the front image to the first page
    if front_image:
        add_image_to_pdf(front_image, 30, height - 30, width * 0.9, height * 0.9)

    # Add the back image to the second page
    if back_image:
        c.showPage()  # Start a new page
        add_image_to_pdf(back_image, 30, height - 30, width * 0.9, height * 0.9)

    # Save the PDF
    c.save()

    # Move the buffer pointer to the beginning
    pdf_buffer.seek(0)
    return pdf_buffer


def upload_media(request, farmer_id):
    farmer = get_object_or_404(Farmer, id=farmer_id)

    if request.method == "POST":
        try:
            # Create a new FarmerMedia instance
            media = FarmerMedia(farmer=farmer)

            # Process and optimize profile picture
            if "picture" in request.FILES:
                optimized = optimize_image(request.FILES["picture"])
                media.picture.save(f"picture_{farmer.id}.jpg", ContentFile(optimized.read()), save=False)
                
            # Handle English EPIC
            if "photo_of_english_epic" in request.FILES:
                english_epic = request.FILES["photo_of_english_epic"]
                # Create both optimized image and PDF version
                optimized = optimize_image(english_epic)
                media.photo_of_english_epic.save(f"epic_en_{farmer.id}.jpg", ContentFile(optimized.read()), save=False)
                
                # Generate PDF for English EPIC
                english_epic.seek(0)  # Reset file pointer
                pdf_buffer = generate_pdf_from_image(english_epic)
                media.english_epic_pdf.save(f"epic_en_{farmer.id}.pdf", ContentFile(pdf_buffer.read()), save=False)
                
            # Handle Regional EPIC
            if "photo_of_regional_language_epic" in request.FILES:
                regional_epic = request.FILES["photo_of_regional_language_epic"]
                # Create both optimized image and PDF version
                optimized = optimize_image(regional_epic)
                media.photo_of_regional_language_epic.save(f"epic_reg_{farmer.id}.jpg", ContentFile(optimized.read()), save=False)
                
                # Generate PDF for Regional EPIC
                regional_epic.seek(0)  # Reset file pointer
                pdf_buffer = generate_pdf_from_image(regional_epic)
                media.regional_epic_pdf.save(f"epic_reg_{farmer.id}.pdf", ContentFile(pdf_buffer.read()), save=False)
                
            # Handle Land Ownership document
            if "land_ownership" in request.FILES:
                land_doc = request.FILES["land_ownership"]
                # Create both optimized image and PDF version
                optimized = optimize_image(land_doc)
                media.land_ownership.save(f"land_{farmer.id}.jpg", ContentFile(optimized.read()), save=False)
                
                # Generate PDF for Land Ownership
                land_doc.seek(0)  # Reset file pointer
                pdf_buffer = generate_pdf_from_image(land_doc)
                media.land_ownership_pdf.save(f"land_{farmer.id}.pdf", ContentFile(pdf_buffer.read()), save=False)
                
            # Handle Tree picture
            if "picture_of_tree" in request.FILES:
                optimized = optimize_image(request.FILES["picture_of_tree"])
                media.picture_of_tree.save(f"tree_{farmer.id}.jpg", ContentFile(optimized.read()), save=False)

            # Handle ID proof generation
            front_image = request.FILES.get("id_proof_front")
            back_image = request.FILES.get("id_proof_back")
            if front_image and back_image:
                # Generate PDF from the uploaded images
                pdf_buffer = generate_pdf_from_images(front_image, back_image)
                pdf_file = ContentFile(pdf_buffer.read(), name=f"id_proof_{farmer.id}.pdf")

                # Save the PDF to the media model
                media.id_proof.save(f"id_proof_{farmer.id}.pdf", pdf_file, save=False)

            # Handle ID type and ID number
            id_type = request.POST.get("id_type")
            id_number = request.POST.get("id_number")
            if id_type:
                media.id_type = id_type
            if id_number:
                media.id_number = id_number

            # Handle digital signature (base64 string from canvas)
            signature_data = request.POST.get("digital_signature")
            if signature_data and ';base64,' in signature_data:
                format, imgstr = signature_data.split(';base64,')
                ext = format.split('/')[-1]
                signature_file = ContentFile(base64.b64decode(imgstr), name=f"signature_{farmer.id}.{ext}")
                media.digital_signature.save(f"signature_{farmer.id}.{ext}", signature_file, save=False)

            # Save the media instance
            media.save()

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