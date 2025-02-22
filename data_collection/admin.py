from django.contrib import admin
from .models import Farmer

class FarmerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "aadhar", "consent_form")  # ✅ Show file field

admin.site.register(Farmer, FarmerAdmin)
