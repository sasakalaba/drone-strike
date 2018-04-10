from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from strike.helpers import Importer


class Command(BaseCommand):
    help = 'Imports json data from https://api.dronestre.am.'

    def handle(self, *args, **options):
        importer = Importer()
        try:
            status = importer.import_data()
            output = (
                'Created/updated: \n\tLocations: %d\n\tCountries: %d\n\tStrikes: %d\n'
                % (status['locations'], status['countries'], status['strikes'])
            )
            self.stdout.write(self.style.SUCCESS(output))
            if status['missing_coor']:
                warning = 'Missing location coordinates: %d.' % status['missing_coor']
                self.stdout.write(self.style.WARNING(warning))
        except ValidationError as error:
            raise CommandError(error.message)
