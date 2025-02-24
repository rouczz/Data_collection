from django.contrib import admin
from .models import Farmer, Farm, Plantation, Specie, GeotaggedSapling

# Register your models here.

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = (
        'aadhar', 'country_id', 'block_id', 'first_name', 'last_name', 'mobile_number', 
        'gender', 'guardian_name', 'geo_tag', 'farmer_consent', 'village', 'pincode', 
        'metadata', 'created_at', 'consent_form'
    )
    list_filter = ('gender', 'farmer_consent', 'village')
    search_fields = ('aadhar', 'first_name', 'last_name', 'mobile_number')
    readonly_fields = ('created_at',)

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = (
        'farmer', 'farm_name', 'area_in_acres', 'ownership', 'owner_mobile_number', 
        'owner_full_name', 'boundary_method', 'boundary', 'metadata'
    )
    list_filter = ('ownership', 'boundary_method')
    search_fields = ('farm_name', 'farmer__first_name', 'farmer__last_name')
    raw_id_fields = ('farmer',)

@admin.register(Plantation)
class PlantationAdmin(admin.ModelAdmin):
    list_display = (
        'farm', 'kyari_name', 'number_of_saplings', 'area_in_acres', 'plantation_model', 
        'year', 'kyari_type', 'is_feasible', 'boundary', 'metadata', 'kyari_attributes'
    )
    list_filter = ('kyari_type', 'is_feasible', 'year')
    search_fields = ('kyari_name', 'farm__farm_name')
    raw_id_fields = ('farm',)

@admin.register(Specie)
class SpecieAdmin(admin.ModelAdmin):
    list_display = (
        'plantation', 'specie_id', 'number_of_plants', 'plant_spacing', 'spacing_cr', 
        'spacing_cl', 'spacing_ct', 'spacing_cb', 'specie_attributes', 'metadata'
    )
    list_filter = ('specie_id',)
    search_fields = ('specie_id', 'plantation__kyari_name')
    raw_id_fields = ('plantation',)

@admin.register(GeotaggedSapling)
class GeotaggedSaplingAdmin(admin.ModelAdmin):
    list_display = ('plantation', 'specie', 'geo_tag', 'metadata')
    list_filter = ('specie',)
    search_fields = ('plantation__kyari_name', 'specie__specie_id')
    raw_id_fields = ('plantation', 'specie')