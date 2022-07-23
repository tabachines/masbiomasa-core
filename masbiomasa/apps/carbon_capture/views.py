"""Views"""
from django.views.generic import DetailView

from .models import Zone


class RasterView(DetailView):
    model = Zone
    template_name = "raster.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        zone = self.object
        context["x"] = zone.polygon.centroid.x
        context["y"] = zone.polygon.centroid.y
        context["feature"] = zone.ndvi_featured
        context["polygon"] = zone.geojson
        return context
