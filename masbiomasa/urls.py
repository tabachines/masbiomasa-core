"""masbiomasa URL Configuration"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from .apps.carbon_capture.views import CalculateNDVIiew

urlpatterns = [
    path("calculate-ndvi/", CalculateNDVIiew.as_view(), name="calculate-ndvi"),
    path(
        "",
        admin.site.urls,
    ),
]

if settings.DEBUG:
    urlpatterns = (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
    )
