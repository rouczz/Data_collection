from django.shortcuts import render, redirect
from .forms import *
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry
from .models import Farmer

def create_farmer(request):
    if request.method == 'POST':
        form = FarmerForm(request.POST)
        lat = request.POST.get('latitude')
        lng = request.POST.get('longitude')
        if form.is_valid() and lat and lng:
            farmer = form.save(commit=False)
            farmer.geo_tag = Point(float(lng), float(lat))  # ✅ Store as GIS Point
            farmer = form.save()
            return redirect('add_farm', farmer_id=farmer.id)  # Redirect to farm creation
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
            return redirect('add_plantation', farm_id=farm.id)  # Redirect to plantation

    else:
        form = FarmForm()

    return render(request, 'data_collection/templates/add_farm.html', {'form': form, 'farmer': farmer})
