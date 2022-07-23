"""Views"""
import json

from django.contrib.gis.geos import GEOSGeometry
from rest_framework.response import Response
from rest_framework.views import APIView

from masbiomasa.apps.carbon_capture.classification import NDVIClassificator
from masbiomasa.apps.carbon_capture.models import Calculation


class CalculateNDVIiew(APIView):
    """Calculate NDVI"""

    def post(self, request, *args, **kwargs):
        """Handle POST requests"""
        geojson = request.data
        geom = GEOSGeometry(json.dumps(geojson.get("geometry")))
        calculation = Calculation(polygon=geom)
        ndvi_raster, ndvi_image, satellite = NDVIClassificator(geom).classify()
        calculation.ndvi_raster = ndvi_raster
        calculation.ndvi_image.save("nvdi.png", ndvi_image)
        calculation.satellite_image.save("satellite.png", satellite)
        calculation.save()
        return Response(
            {
                "ndvi_url": calculation.ndvi_image.url,
                "satellite_url": calculation.satellite_image.url,
                "center": json.loads(calculation.polygon.centroid.json).get(
                    "coordinates"
                ),
                "bounds": list(calculation.polygon.extent),
            }
        )
