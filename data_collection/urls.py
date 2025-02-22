from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', create_farmer, name='create_farmer'),
    path('add_farm/<int:farmer_id>/', add_farm, name='add_farm'),
    path('add-plantation/<int:farm_id>/', add_plantation, name='add_plantation'),
    path('add-species/<int:plantation_id>/', add_specie, name='add_specie'),
    path("dashboard-data/<int:farmer_id>/", get_farmer_details, name="dashboard_data"),
    path("dashboard-farmers/", get_farmers_list, name="dashboard_farmers"),
    path('dashboard/', dashboard, name='dashboard'),
]
# Compare this snippet from KMcollect/data_collection/views.py: 

if settings.DEBUG:  # Serve static and media files in development
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)