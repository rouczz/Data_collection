from django.urls import path
from .views import *

urlpatterns = [
    path('create_farmer/', create_farmer, name='create_farmer'),
    path('add_farm/<int:farmer_id>/', add_farm, name='add_farm'),
    
    # path('add_plantation/<int:farm_id>/', add_plantation, name='add_plantation'),
    # path('add_specie/<int:plantation_id>/', add_specie, name='add_specie'),
]
# Compare this snippet from KMcollect/data_collection/views.py: 