import json
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from urllib.request import urlopen
from .models import Country
from .serializers import StrikeSerializer, LocationSerializer


class Importer(object):
    """
    JSON importer class.
    """

    def __init__(self, *args, **kwargs):
        self.location_keys = ['lat', 'lon', 'country', 'town', 'location']
        self.data_url = settings.STRIKE_DATA_URL
        self.data = None

    def parse_date(self, date_str):
        """
        Return a date object from date string.
        """
        return datetime.strptime(date_str, settings.DATE_FORMAT).date()

    def get_json(self):
        """
        Download valid JSON data.
        """
        response = urlopen(self.data_url)
        if response.code != 200:
            return {'success': False, 'error': 'Bad request.'}
        try:
            data = json.loads(response.read().decode())
        except json.JSONDecodeError:
            return {'success': False, 'error': 'Not a valid JSON file.'}

        if data['status'] != 'OK':
            return {'success': False, 'error': 'Data not valid.'}

        self.data = {'success': True, 'data': data}
        return self.data


    def import_data(self):
        """
        Main import method.
        """
        # Load json_data if not already loaded.
        if self.data is None:
            json_data = self.get_json()
            if not json_data['success']:
                raise ValidationError(json_data['error'])

        with transaction.atomic():
            counter = {
                'countries': 0,
                'locations': 0,
                'strikes': 0,
                'missing_coor': 0,
            }

            # Copy the list
            strikes = self.data['data']['strike'][:]

            for strike in strikes:
                # Set location_data
                location_data = {}
                for key in self.location_keys:
                    location_data[key] = strike.pop(key, None)

                # Set strike data
                strike.pop('_id')
                strike['date'] = self.parse_date(strike['date'])

                # Create country, and update counter and fk.
                country, created = Country.objects.get_or_create(
                    name=location_data.pop('country', None))
                location_data['country'] = country.id
                if created:
                    counter['countries'] += 1

                # TODO: move this to serializer
                if location_data['lat'] == '':
                    location_data['lat'] = None
                    counter['missing_coor'] += 1
                if location_data['lon'] == '':
                    location_data['lon'] = None

                # Create location, and update counter and fk.
                serializer = LocationSerializer(data=location_data)
                if serializer.is_valid():
                    location_id = serializer.save().id
                    counter['locations'] += 1
                else:
                    location_id = str(serializer.errors['instance'][0])

                # Create strike and update counter.
                strike['location'] = location_id
                serializer = StrikeSerializer(data=strike)
                if serializer.is_valid():
                    serializer.save()
                    counter['strikes'] += 1

        return counter
