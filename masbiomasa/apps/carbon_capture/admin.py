"""Admin models"""

from django.contrib import admin

from .models import Calculation, LandVegetation


@admin.register(LandVegetation)
class LandVegetationAdmin(admin.ModelAdmin):
    """LandVegetation admin model"""

    list_display = ("name",)


@admin.register(Calculation)
class CalculationAdmin(admin.ModelAdmin):
    """Calculation admin model"""

    list_display = ("name",)
