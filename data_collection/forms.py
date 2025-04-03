from django import forms
from .models import Farmer
import re
class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = [ 'first_name', 'last_name', 'mobile_number', 'gender', 
                  'guardian_name', 'village', 'pincode', 'farmer_consent']  # ✅ Removed `geo_tag`
        widgets = {
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]),
            # 'farmer_consent': forms.CheckboxInput(),
        }


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
        exclude = ['boundary','farmer']  # Exclude boundary since it's handled via map drawing
        widgets = {
            'ownership': forms.Select(choices=[('OWNED', 'Owned'), ('LEASED', 'Leased')]),
            'boundary_method': forms.Select(choices=[('Drawing', 'Drawing'), ('Tapping', 'Tapping')]),
            'owner_mobile_number': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Owner Mobile Number"}),
            'owner_full_name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Owner Full Name"}),
            'landlord_declaration': forms.ClearableFileInput(attrs={"accept": "image/*", "capture": "environment"}),
            'land_ownership': forms.ClearableFileInput(attrs={"accept": "image/*", "capture": "environment"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initially hide fields for leased farms
        if 'ownership' in self.initial and self.initial['ownership'] == 'LEASED':
            self.fields['owner_mobile_number'].required = True
            self.fields['owner_full_name'].required = True
            self.fields['landlord_declaration'].required = True
        else:
            self.fields['owner_mobile_number'].required = False
            self.fields['owner_full_name'].required = False
            self.fields['landlord_declaration'].required = False

from django import forms
from .models import Plantation

class PlantationForm(forms.ModelForm):
    class Meta:
        model = Plantation
        exclude = ["boundary"]  # We will handle boundary using Leaflet map
        fields = ['kyari_name', 'area_in_acres','plantation_year', 'boundary']


from django import forms
from .models import Specie

class SpecieForm(forms.ModelForm):
    class Meta:
        model = Specie
        exclude = ["plantation"] 
        fields = "__all__"
        widgets = {
            'plantation_date': forms.DateInput(attrs={'type': 'date'}),
        }



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
            'id_expiry_date',
        
            'digital_signature'
        ]
        widgets = {
            'picture': forms.ClearableFileInput(attrs={"accept": "image/*", "capture": "environment"}),
            'photo_of_english_epic': forms.ClearableFileInput(attrs={"accept": "application/pdf"}),
            'photo_of_regional_language_epic': forms.ClearableFileInput(attrs={"accept": "application/pdf"}),
            'id_type': forms.Select(attrs={"class": "form-control"}),
            'id_number': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter ID Number"}),
            'id_proof': forms.ClearableFileInput(attrs={"accept": "application/pdf"}),
            
            'digital_signature': forms.HiddenInput(),  # Hidden input for base64 signature
        }