from django.contrib.gis.db import models

class Farmer(models.Model):
    aadhar = models.CharField(max_length=16, unique=True)
    country_id = models.IntegerField(default=1)
    block_id = models.IntegerField(default=0)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    guardian_name = models.CharField(max_length=100, blank=True)
    geo_tag = models.PointField()
    farmer_consent = models.BooleanField(default=False)
    village = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    metadata = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    consent_form = models.FileField(upload_to="consent_forms/", null=True, blank=True)  # ✅ New file field

    def __str__(self):
        return f"{self.first_name} {self.last_name}"  

class Farm(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='farms')
    farm_name = models.CharField(max_length=100)
    area_in_acres = models.FloatField()
    ownership = models.CharField(max_length=10, choices=[('OWNED', 'Owned'), ('LEASED', 'Leased')])
    owner_mobile_number = models.CharField(max_length=15, blank=True, null=True)
    owner_full_name = models.CharField(max_length=100, blank=True, null=True)
    boundary_method = models.CharField(max_length=10, choices=[('Drawing', 'Drawing'), ('Tapping', 'Tapping')])
    boundary = models.PolygonField()
    metadata = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return self.farm_name

class Plantation(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='plantations')
    kyari_name = models.CharField(max_length=100)
    number_of_saplings = models.IntegerField()
    area_in_acres = models.FloatField()
    plantation_model = models.CharField(max_length=50, choices=[('BLOCK', 'Block')], blank=True, null=True)
    year = models.IntegerField()
    kyari_type = models.CharField(max_length=50, choices=[('RETROSPECTIVE', 'Retrospective'), ('PLANTATION', 'Plantation')])
    is_feasible = models.BooleanField(default=True)
    boundary = models.PolygonField()
    metadata = models.JSONField(default=dict, blank=True, null=True)
    kyari_attributes = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return self.kyari_name

class Specie(models.Model):
    plantation = models.ForeignKey(Plantation, on_delete=models.CASCADE, related_name='species')
    specie_id = models.IntegerField()
    number_of_plants = models.IntegerField()
    plant_spacing = models.CharField(max_length=10)
    spacing_cr = models.FloatField()
    spacing_cl = models.FloatField()
    spacing_ct = models.FloatField()
    spacing_cb = models.FloatField()
    specie_attributes = models.JSONField(default=dict, blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return f"Specie {self.specie_id} in {self.plantation.kyari_name}"

class GeotaggedSapling(models.Model):
    plantation = models.ForeignKey(Plantation, on_delete=models.CASCADE, related_name='saplings')
    specie = models.ForeignKey(Specie, on_delete=models.CASCADE, related_name='saplings')
    geo_tag = models.PointField()
    metadata = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return f"Sapling in {self.plantation.kyari_name}"
