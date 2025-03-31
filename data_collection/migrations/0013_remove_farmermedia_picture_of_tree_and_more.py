# Generated by Django 5.1.6 on 2025-03-31 11:45

import data_collection.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_collection', '0012_farmermedia_id_expiry_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='farmermedia',
            name='picture_of_tree',
        ),
        migrations.AddField(
            model_name='farmermedia',
            name='centre_bottom',
            field=models.ImageField(blank=True, null=True, upload_to=data_collection.models.farmer_media_path),
        ),
        migrations.AddField(
            model_name='farmermedia',
            name='centre_left',
            field=models.ImageField(blank=True, null=True, upload_to=data_collection.models.farmer_media_path),
        ),
        migrations.AddField(
            model_name='farmermedia',
            name='centre_right',
            field=models.ImageField(blank=True, null=True, upload_to=data_collection.models.farmer_media_path),
        ),
        migrations.AddField(
            model_name='farmermedia',
            name='centre_top',
            field=models.ImageField(blank=True, null=True, upload_to=data_collection.models.farmer_media_path),
        ),
    ]
