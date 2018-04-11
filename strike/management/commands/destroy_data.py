from django.core.management.base import BaseCommand
from strike.models import Strike, Location, Country


class Command(BaseCommand):
    help = 'Deletes strike objects from the database.'

    def handle(self, *args, **options):
        Strike.objects.all().delete()
        Location.objects.all().delete()
        Country.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Strike objects successfully deleted.'))
