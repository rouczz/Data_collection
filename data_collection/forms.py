from django import forms
from .models import Farmer

class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        exclude = ['geo_tag']
        fields = ['aadhar', 'first_name', 'last_name', 'mobile_number', 'gender', 'guardian_name', 'geo_tag', 'village', 'pincode', 'farmer_consent']
        widgets = {
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]),
            'farmer_consent': forms.CheckboxInput(),
        }


from .models import Farm

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        exclude = ['boundary']
        fields = ['farm_name', 'area_in_acres', 'ownership', 'boundary_method', 'boundary']
        widgets = {
            'ownership': forms.Select(choices=[('OWNED', 'Owned'), ('LEASED', 'Leased')]),
            'boundary_method': forms.Select(choices=[('Drawing', 'Drawing'), ('Tapping', 'Tapping')]),
        }

from django import forms
from .models import Plantation

class PlantationForm(forms.ModelForm):
    class Meta:
        model = Plantation
        exclude = ["boundary"]  # We will handle boundary using Leaflet map
        fields = ['kyari_name', 'number_of_saplings', 'area_in_acres', 'plantation_model', 'year', 'kyari_type', 'is_feasible', 'boundary']


from django import forms
from .models import Specie

class SpecieForm(forms.ModelForm):
    class Meta:
        model = Specie
        exclude = ["plantation"] 
        fields = "__all__"
