# Generated by Django 4.0.6 on 2022-07-23 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carbon_capture', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculation',
            name='satellite_image',
            field=models.ImageField(blank=True, null=True, upload_to='satellite_images/'),
        ),
    ]