"""Carbon capture models"""

from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


class LandVegetation(models.Model):
    """Land vegetation properties for calculartions"""

    name = models.CharField(max_length=255)
    ndvi_min_value = models.FloatField(default=0)
    ndvi_max_value = models.FloatField(default=1)
    carbon_capture_per_ha = models.FloatField(default=0)
    images = models.ImageField(upload_to="vegetation_images/", null=True, blank=True)
    description = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        """Meta definitions"""

        verbose_name = _("Land vegetation")
        verbose_name_plural = _("Land vegetations")


class Calculation(models.Model):
    """Carbon capture calculation model"""

    name = models.CharField(max_length=50)
    polygon = models.PolygonField()
    ndvi_raster = models.FileField(upload_to="ndvi_rasters/", null=True, blank=True)
    carbon_capture_raster = models.FileField(
        upload_to="carbon_capture_rasters/", null=True, blank=True
    )
    ndvi_image = models.ImageField(upload_to="ndvi_images/", null=True, blank=True)
    satellite_image = models.ImageField(
        upload_to="satellite_images/", null=True, blank=True
    )
    carbon_capture_image = models.ImageField(
        upload_to="carbon_capture_images/", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        """Meta definition for Calculation."""

        verbose_name = _("Land vegetation")
        verbose_name_plural = _("Land vegetations")
