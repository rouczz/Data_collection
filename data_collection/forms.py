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
