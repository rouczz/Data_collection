# Generated by Django 5.1.6 on 2025-02-10 10:49

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Farmer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aadhar', models.CharField(max_length=16, unique=True)),
                ('country_id', models.IntegerField()),
                ('block_id', models.IntegerField()),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('mobile_number', models.CharField(max_length=15)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10)),
                ('guardian_name', models.CharField(blank=True, max_length=100)),
                ('geo_tag', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('farmer_consent', models.BooleanField(default=False)),
                ('village', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=10)),
                ('metadata', models.JSONField(blank=True, default=dict, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Farm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('farm_name', models.CharField(max_length=100)),
                ('area_in_acres', models.FloatField()),
                ('ownership', models.CharField(choices=[('OWNED', 'Owned'), ('LEASED', 'Leased')], max_length=10)),
                ('owner_mobile_number', models.CharField(blank=True, max_length=15, null=True)),
                ('owner_full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('boundary_method', models.CharField(choices=[('Drawing', 'Drawing'), ('Tapping', 'Tapping')], max_length=10)),
                ('boundary', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('metadata', models.JSONField(blank=True, default=dict, null=True)),
                ('farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='farms', to='data_collection.farmer')),
            ],
        ),
        migrations.CreateModel(
            name='Plantation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kyari_name', models.CharField(max_length=100)),
                ('number_of_saplings', models.IntegerField()),
                ('area_in_acres', models.FloatField()),
                ('plantation_model', models.CharField(blank=True, choices=[('BLOCK', 'Block')], max_length=50, null=True)),
                ('year', models.IntegerField()),
                ('kyari_type', models.CharField(choices=[('RETROSPECTIVE', 'Retrospective'), ('PLANTATION', 'Plantation')], max_length=50)),
                ('is_feasible', models.BooleanField(default=True)),
                ('boundary', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('metadata', models.JSONField(blank=True, default=dict, null=True)),
                ('kyari_attributes', models.JSONField(blank=True, default=dict, null=True)),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plantations', to='data_collection.farm')),
            ],
        ),
        migrations.CreateModel(
            name='Specie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specie_id', models.IntegerField()),
                ('number_of_plants', models.IntegerField()),
                ('plant_spacing', models.CharField(max_length=10)),
                ('spacing_cr', models.FloatField()),
                ('spacing_cl', models.FloatField()),
                ('spacing_ct', models.FloatField()),
                ('spacing_cb', models.FloatField()),
                ('specie_attributes', models.JSONField(blank=True, default=dict, null=True)),
                ('metadata', models.JSONField(blank=True, default=dict, null=True)),
                ('plantation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='species', to='data_collection.plantation')),
            ],
        ),
        migrations.CreateModel(
            name='GeotaggedSapling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geo_tag', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('metadata', models.JSONField(blank=True, default=dict, null=True)),
                ('plantation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saplings', to='data_collection.plantation')),
                ('specie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saplings', to='data_collection.specie')),
            ],
        ),
    ]
