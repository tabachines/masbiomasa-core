"""Coverland classification."""
import io
import json
from zipfile import ZipFile

import ee
import requests
from django.conf import settings
from django.contrib.gis.db.models import PolygonField
from django.core.files import File

ee.Initialize(settings.GOOGLE_EARTH_CREDENTIALS)


def get_file(file_url, zipped=False, extension=".tif"):
    """Get first file from a zip archive."""
    response = requests.get(file_url)
    if zipped:
        zipfile = ZipFile(io.BytesIO(response.content))
        file_name = zipfile.namelist()[0]
        file = zipfile.open(file_name)
    else:
        file = io.BytesIO(response.content)
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
            .first()
            .clip(self.geometry)
        )
        ndvi = img.normalizedDifference(["B8", "B4"])

        image_url = ndvi.getDownloadUrl(
            {
                "region": self.geometry,
                "scale": 1000,
            }
        )
        raster_file = get_file(image_url, zipped=True)
        return File(raster_file)
