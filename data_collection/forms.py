from django import forms
from .models import Farmer
import re
class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['aadhar', 'first_name', 'last_name', 'mobile_number', 'gender', 
                  'guardian_name', 'village', 'pincode', 'farmer_consent']  # ✅ Removed `geo_tag`
        widgets = {
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]),
            # 'farmer_consent': forms.CheckboxInput(),
        }

    def clean_aadhar(self):
        aadhar = self.cleaned_data.get("aadhar")
        if not re.fullmatch(r"\d{12}", aadhar):  # ✅ Ensures exactly 12 digits
            raise forms.ValidationError("Aadhaar number must be a 12-digit integer.")
        return aadhar

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get("mobile_number")
        if not re.fullmatch(r"\d{10}", mobile_number):  # ✅ Ensures exactly 10 digits
            raise forms.ValidationError("Mobile number must be a 10-digit integer.")
        return mobile_number

    def clean_pincode(self):
        pincode = self.cleaned_data.get("pincode")
        if not re.fullmatch(r"\d{6}", pincode):  # ✅ Ensures exactly 6 digits
            raise forms.ValidationError("Pincode must be a 6-digit integer.")
        return pincode

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


from django import forms
from .models import FarmerMedia

class FarmerMediaForm(forms.ModelForm):
    class Meta:
        model = FarmerMedia
        fields = [
            'picture',
            'photo_of_english_epic',
            'photo_of_regional_language_epic',
            'id_type',
            'id_number',
            'id_proof',
            'land_ownership',
            'picture_of_tree',
            'digital_signature'
        ]
        widgets = {
            'picture': forms.ClearableFileInput(attrs={"accept": "image/*", "capture": "environment"}),
            'photo_of_english_epic': forms.ClearableFileInput(attrs={"accept": "application/pdf"}),
            'photo_of_regional_language_epic': forms.ClearableFileInput(attrs={"accept": "application/pdf"}),
            'id_type': forms.Select(attrs={"class": "form-control"}),
            'id_number': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter ID Number"}),
            'id_proof': forms.ClearableFileInput(attrs={"accept": "application/pdf"}),
            'land_ownership': forms.ClearableFileInput(attrs={"accept": "application/pdf,.doc,.docx"}),
            'picture_of_tree': forms.ClearableFileInput(attrs={"accept": "image/*", "capture": "environment"}),
            'digital_signature': forms.HiddenInput(),  # Hidden input for base64 signature
        }