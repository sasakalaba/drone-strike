import json
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from urllib.request import urlopen
from .models import Strike, Location, Country


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

        # TODO: Test this with invalid data
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
                location, created = Location.objects.get_or_create(
                    country=country, **location_data)
                Strike.objects.create(location=location, **strike)


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
