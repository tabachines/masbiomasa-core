"""Coverland classification."""
import io
import json
from zipfile import ZipFile

import ee
import requests
from django.conf import settings
from django.contrib.gis.db.models import PolygonField
from django.core.files import File
from django.core.files.base import ContentFile

ee.Initialize(settings.GOOGLE_EARTH_CREDENTIALS)


def get_file(file_url, zipped=False, extension=".tif"):
    """Get first file from a zip archive."""
    response = requests.get(file_url)
    if zipped:
        zipfile = ZipFile(io.BytesIO(response.content))
        file_name = zipfile.namelist()[0]
        file = zipfile.open(file_name)
    else:
        file = ZipFile(response.content)
    return file


class NDVIClassificator:
    """K-means classificator."""

    geometry = None
    k = None

    def __init__(self, geometry: PolygonField, k=2):
        """Initialize classificator."""
        self.geometry = ee.Geometry(json.loads(geometry.geojson))
        self.k = k

    def classify(
        self,
    ):
        """Get sattelite image."""
        img = (
            ee.ImageCollection("COPERNICUS/S2_SR")
            .filterDate("2020-01-01", "2021-12-30")
            .filterBounds(self.geometry)
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 10))
            .sort("date", False)
            .mean()
        )
        img_clipped = img.clip(self.geometry)
        ndvi = img_clipped.normalizedDifference(["B8", "B4"])

        satellite_image_url = img_clipped.getThumbURL(
            {
                "bands": ["B4", "B3", "B2"],
                "region": self.geometry,
                "dimensions": 256,
                "format": "png",
                "gamma": 1.0,
                "max": 4000,
                "min": 0.0,
            }
        )

        nvdi_image_url = ndvi.getThumbURL(
            {
                "region": self.geometry,
                "dimensions": 256,
                "format": "png",
                "max": 1.0,
                "min": -1.0,
                "palette": [
                    "FFFFFF",
                    "CE7E45",
                    "DF923D",
                    "F1B555",
                    "FCD163",
                    "99B718",
                    "74A901",
                    "66A000",
                    "529400",
                    "3E8601",
                    "207401",
                    "056201",
                    "004C00",
                    "023B01",
                    "012E01",
                    "011D01",
                    "011301",
                ],
            }
        )
        raster_url = ndvi.getDownloadUrl(
            {
                "region": self.geometry,
                "scale": 1000,
            }
        )
        image = requests.get(nvdi_image_url).content
        satellite_image = requests.get(satellite_image_url).content
        raster_file = get_file(raster_url, zipped=True)
        return File(raster_file), ContentFile(image), ContentFile(satellite_image)
