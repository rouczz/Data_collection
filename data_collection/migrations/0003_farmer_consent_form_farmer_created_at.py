# Generated by Django 5.1.6 on 2025-02-22 08:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_collection', '0002_alter_farmer_block_id_alter_farmer_country_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmer',
            name='consent_form',
            field=models.FileField(blank=True, null=True, upload_to='consent_forms/'),
        ),
        migrations.AddField(
            model_name='farmer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
