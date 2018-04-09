from django.core.management.base import BaseCommand, CommandError
from strike.helpers import Importer


class Command(BaseCommand):
    help = 'Imports json data from https://api.dronestre.am.'

    def handle(self, *args, **options):
        # importer = Importer()
        # status = importer.import_data(destroy=options['delete'])

        # TODO: implement your own messages
        """
        if type(status) is str:
            self.stdout.write(self.style.SUCCESS(status))
        else:
            raise CommandError(str(status))
        """
