from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from .postapi import *
from .vaarha_api import *

urlpatterns = [
    path('', create_farmer, name='create_farmer'),
    path('add_farm/<int:farmer_id>/', add_farm, name='add_farm'),
    path("api/farms/<int:farmer_id>/", get_farms_for_farmer, name="get_farms"),
    path('add-plantation/<int:farmer_id>/', add_plantation, name='add_plantation'),
    path('add-species/<int:farmer_id>/', add_specie, name='add_specie'),
    path("dashboard-data/<int:farmer_id>/", get_farmer_details, name="dashboard_data"),
    path("dashboard-farmers/", get_farmers_list, name="dashboard_farmers"),
    path('dashboard/', dashboard, name='dashboard'),
    path('get-plantations/<int:farm_id>/', get_plantations_for_farm, name='get_plantations_for_farm'),
    path("upload-media/<int:farmer_id>/", upload_media, name="upload_media"),



    #POST API 
    path('send-farmer/<int:farmer_id>/', send_farmer_data, name='send_farmer_data'),


    #Get API call from Vaarha
    path("api/states/", get_states, name="get_states"),
    path("api/districts/<int:state_id>/",get_districts, name="get_districts"),
    path("api/blocks/<int:district_id>/",get_blocks, name="get_blocks"),
    path("api/plantation/species/all/", get_species, name="get_species"),
]
# Compare this snippet from KMcollect/data_collection/views.py: 

if settings.DEBUG:  # Serve static and media files in development
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)