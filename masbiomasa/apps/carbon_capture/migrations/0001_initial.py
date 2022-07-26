# Generated by Django 4.0.6 on 2022-07-23 13:29

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Calculation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('polygon', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('ndvi_raster', models.FileField(blank=True, null=True, upload_to='ndvi_rasters/')),
                ('carbon_capture_raster', models.FileField(blank=True, null=True, upload_to='carbon_capture_rasters/')),
                ('ndvi_image', models.ImageField(blank=True, null=True, upload_to='ndvi_images/')),
                ('carbon_capture_image', models.ImageField(blank=True, null=True, upload_to='carbon_capture_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Land vegetation',
                'verbose_name_plural': 'Land vegetations',
            },
        ),
        migrations.CreateModel(
            name='LandVegetation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('ndvi_min_value', models.FloatField(default=0)),
                ('ndvi_max_value', models.FloatField(default=1)),
                ('carbon_capture_per_ha', models.FloatField(default=0)),
                ('images', models.ImageField(blank=True, null=True, upload_to='vegetation_images/')),
                ('description', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name': 'Land vegetation',
                'verbose_name_plural': 'Land vegetations',
            },
        ),
    ]
