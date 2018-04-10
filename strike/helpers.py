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
            # TODO: maybe just let JSONDecodeError do its thing here.
            return {'success': False, 'error': 'Not a valid JSON file.'}

        if data['status'] != 'OK':
            return {'success': False, 'error': 'Data not valid.'}

        self.data = {'success': True, 'data': data}
        return self.data


    def import_data(self):
        """
        Main import method.
        """

        if self.data is None:
            json_data = self.get_json()
            if not json_data['success']:
                raise ValidationError(json_data['error'])

        with transaction.atomic():
            # Copy the list
            strikes = self.data['data']['strike'][:]

            for strike in strikes:
                location_data = {}
                for key in self.location_keys:
                    location_data[key] = strike.pop(key, None)
                strike.pop('_id')
                strike['date'] = self.parse_date(strike['date'])
                country, created = Country.objects.get_or_create(
                    name=location_data.pop('country', None))
                location_data['country'] = country.id

                # TODO: move this to serializer
                if location_data['lat'] == '':
                    location_data['lat'] = None
                if location_data['lon'] == '':
                    location_data['lon'] = None

                serializer = LocationSerializer(data=location_data)
                if serializer.is_valid():
                    location_id = serializer.save().id
                else:
                    location_id = str(serializer.errors['instance'][0])
                    print(serializer.errors['error'])

                strike['location'] = location_id
                serializer = StrikeSerializer(data=strike)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)


        # TODO: implement counter
        """
        update_counter = {
            'created': self.counter['created'],
            'updated': self.counter['updated'],
        }
        """

        # TODO: return message
        """
        return (
            'Beers:\n\tCreated: %s \n\tUpdated: %s \n' % (
                update_counter['created'],
                update_counter['updated'],
                update_counter['no_coordinates']
            )
        )
        """
        pass
