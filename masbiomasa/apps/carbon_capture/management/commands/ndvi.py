"""NDVI calculation command"""

from django.core.management.base import BaseCommand, CommandError

from masbiomasa.apps.carbon_capture.classification import NDVIClassificator
from masbiomasa.apps.carbon_capture.models import Calculation


class Command(BaseCommand):
    """NDVI calculation command"""

    help = "Recalculate NDVI for a zone"

    def add_arguments(self, parser):
        """Add arguments to the command parser"""
        parser.add_argument("zone_id", type=int)

    def handle(self, *args, **options):
        """Handle the command"""
        try:
            zone_id = options["zone_id"]
            zone = Calculation.objects.get(pk=zone_id)
            classificator = NDVIClassificator(zone.polygon)
            raster = classificator.classify()
            zone.ndvi = raster
            zone.save()
        except Calculation.DoesNotExist:
            raise CommandError('Zone "%s" does not exist' % zone_id)

        zone.save()

        self.stdout.write(
            self.style.SUCCESS('Successfully updated NDVI "%s"' % zone.name)
        )
