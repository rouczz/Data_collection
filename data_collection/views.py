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
    farmer = Farmer.objects.get(id=farmer_id)

    if request.method == 'POST':
        form = FarmForm(request.POST)
        boundary_geojson = request.POST.get('boundary')
        
        if form.is_valid():
            farm = form.save(commit=False)
            farm.farmer = farmer
            farm = form.save(commit=False)
            farm.farmer = farmer
            farm.boundary = GEOSGeometry(boundary_geojson) 
            farm.save()
            return JsonResponse({'success': True, 'farm_id': farm.id})

    else:
        form = FarmForm()

    return render(request, 'data_collection/templates/add_farm.html', {'form': form, 'farmer': farmer})

def add_plantation(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)

    if request.method == "POST":
        form = PlantationForm(request.POST)
        boundary_geojson = request.POST.get("boundary")

        if form.is_valid() and boundary_geojson:
            plantation = form.save(commit=False)
            plantation.farm = farm
            plantation.boundary = GEOSGeometry(boundary_geojson)  # ✅ Convert GeoJSON to Polygon
            plantation.save()
            return JsonResponse({"success": True, "plantation_id": plantation.id})

        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    else:
        form = PlantationForm()

    return render(request, "data_collection/templates/add_plantation.html", {"form": form, "farm": farm})


def add_specie(request, plantation_id):
    plantation = get_object_or_404(Plantation, id=plantation_id)
    print(f"Plantation: {plantation}")
    if request.method == "POST":
        form = SpecieForm(request.POST)
        if form.is_valid():
            specie = form.save(commit=False)
            specie.plantation = plantation
            specie.save()
            return JsonResponse({"success": True, "specie_id": specie.id})

        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    else:
        form = SpecieForm()

    return render(request, "data_collection/templates/add_specie.html", {"form": form, "plantation": plantation})

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

