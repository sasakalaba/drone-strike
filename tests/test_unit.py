import freezegun
import json
import mock
from datetime import date
from django.conf import settings
from django.core.exceptions import ValidationError
from django.urls import reverse
from strike.helpers import Importer
from strike.models import Location, Country, Strike
from strike.serializers import LocationSerializer
from strike.views import IndexView
from rest_framework import exceptions
from .base import BaseTestCase


class ImporterTest(BaseTestCase):
    """
    Unit tests for import data helper function.
    """

    def setUp(self):
        super(ImporterTest, self).setUp()
        self.importer = Importer()
        self.importer.data_url = None
        self.test_data = {
            'success': True,
            'data': {
                'status': '0K',
                'strike': [{
                    '_id': '55c79e711cbee48856a30886',
                    'articles': [],
                    'bij_link': 'http://www.thebureauinvestigates.com/2012/03/29/yemen-reported-us-covert-actions-since-2001/',
                    'bij_summary_short': 'In the first known US targeted assassination using a '
                                         'drone, a CIA Predator struck a car killing six al Qaeda '
                                         'suspects.',
                    'bureau_id': 'YEM001',
                    'children': '',
                    'civilians': '0',
                    'country': 'Yemen',
                    'date': '2002-11-03T00:00:00.000Z',
                    'deaths': '6',
                    'deaths_max': '6',
                    'deaths_min': '6',
                    'injuries': '',
                    'location': 'Marib Province',
                    'lat': '15.47467',
                    'lon': '45.322755',
                    'names': ["Qa'id Salim Sinan al-Harithi, Abu Ahmad al-Hijazi, Salih Hussain "
                              'Ali al-Nunu, Awsan Ahmad al-Tarihi, Munir Ahmad Abdallah al-Sauda, '
                              "Adil Nasir al-Sauda'"],
                    'narrative': 'In the first known US targeted assassination using a drone, a '
                                 'CIA Predator struck a car, killing 6 people.',
                    'number': 1,
                    'target': '',
                    'town': '',
                    'tweet_id': '278544689483890688'
                }, {
                    '_id': '55c79e711cbee48856a30887',
                    'articles': [],
                    'bij_link': 'http://www.thebureauinvestigates.com/2011/08/10/the-bush-years-2004-2009/',
                    'bij_summary_short': 'First known drone strike in Pakistan kills at least '
                                         'six, including infamous Taliban leader Nek Mohammad and '
                                         'two children. Wana, South Waziristan.',
                    'bureau_id': 'B1',
                    'children': '2',
                    'civilians': '2',
                    'country': 'Pakistan',
                    'date': '2004-06-17T00:00:00.000Z',
                    'deaths': '6-8',
                    'deaths_max': '8',
                    'deaths_min': '6',
                    'injuries': '1',
                    'location': 'South Waziristan',
                    'lat': '',
                    'lon': '',
                    'names': ['Nek Mohammad, Fakhar Zaman, Azmat Khan, Marez Khan, Shahrukh Khan, '
                              'Leetak, Sher Zaman Ashrafkhel'],
                    'narrative': 'The first known fatal US drone strike inside Pakistan killed '
                                 '6-8 people, including 2 children.',
                    'number': 2,
                    'target': 'Nek Mohammed',
                    'town': 'Wana',
                    'tweet_id': '278544750867533824'
                }]
            }
        }

    def test_parse_date(self):
        """
        Extract proper date objects from date strings.
        """
        date_str = '2002-11-03T00:00:00.000Z'
        self.assertEqual(self.importer.parse_date(date_str), date(2002, 11, 3))

    @mock.patch('strike.helpers.urlopen')
    def test_get_json_bad_request(self, urlopen):
        """
        get_json bad request.
        """
        class ResponseInvalid(object):
            code = 400

        response = ResponseInvalid()
        urlopen.return_value = response
        status = self.importer.get_json()
        self.assertDictEqual(status, {'success': False, 'error': 'Bad request.'})

    @mock.patch('strike.helpers.urlopen')
    def test_get_json_invalid_json(self, urlopen):
        """
        get_json invalid JSON file.
        """
        class Doc(object):
            def count(self, *args, **kargs):
                return 1

            def rfind(self, *args, **kargs):
                return 0

        class ResponseInvalid(object):
            code = 200

            def read(self):
                raise json.JSONDecodeError(msg='', doc=Doc(), pos=3)

        response = ResponseInvalid()
        urlopen.return_value = response
        status = self.importer.get_json()
        self.assertDictEqual(
            status, {'success': False, 'error': 'Not a valid JSON file.'})

    @mock.patch('strike.helpers.urlopen')
    def test_get_json_invalid_data(self, urlopen):
        """
        get_json invalid data.
        """
        class ResponseInvalidData(object):
            code = 200

            def read(self):
                return '{"status": "NOT OK", "foo": "bar"}'.encode()

        response = ResponseInvalidData()
        urlopen.return_value = response
        status = self.importer.get_json()
        self.assertDictEqual(
            status, {'success': False, 'error': 'Data not valid.'})

    @mock.patch('strike.helpers.urlopen')
    def test_get_json_success(self, urlopen):
        """
        get_json success.
        """
        class Response(object):
            code = 200

            def read(self):
                return '{"status": "OK", "foo": "bar"}'.encode()

        response = Response()
        urlopen.return_value = response
        status = self.importer.get_json()
        self.assertDictEqual(
            status, {'success': True, 'data': {"status": "OK", "foo": "bar"}})

    @mock.patch('strike.helpers.urlopen')
    def test_import_data_get_json(self, urlopen):
        """
        Make sure that get_json is called if JSON data is not loaded.
        """
        class ResponseInvalidData(object):
            code = 200

            def read(self):
                return '{"status": "NOT OK", "foo": "bar"}'.encode()

        response = ResponseInvalidData()
        urlopen.return_value = response

        # Reinit importer.
        self.importer = Importer()
        self.data_url = None

        # Make sure that get_json was called.
        with self.assertRaises(ValidationError) as error:
            self.importer.import_data()
        self.assertEqual(error.exception.message, 'Data not valid.')

    def test_import_data_empty_coor(self):
        """
        Make sure empty coordinates and all related data are not imported.
        """
        self.country.delete()
        self.importer.data = self.test_data
        counter = self.importer.import_data()
        self.assertDictEqual(
            counter,
            {'locations': 1, 'strikes': 1, 'countries': 1, 'missing_coor': 1}
        )

        # Ensure that counters are correct.
        Location.objects.get(), Strike.objects.get(), Country.objects.get()

    def test_import_data_country_created(self):
        """
        Make sure that countries aren't duplicated, and related data is properly
        mapped to existing country instance.
        """
        strike_data = self.test_data['data']['strike'][1]
        strike_data['country'] = 'Yemen'
        strike_data['lat'] = '16.66666'
        strike_data['lon'] = '47.777777'

        self.country.delete()
        self.importer.data = self.test_data
        counter = self.importer.import_data()
        self.assertDictEqual(
            counter,
            {'locations': 2, 'strikes': 2, 'countries': 1, 'missing_coor': 0}
        )

        # Ensure that counters are correct.
        self.assertEqual(Location.objects.count(), 2)
        self.assertEqual(Strike.objects.count(), 2)
        Country.objects.get()

    def test_import_data_location_created(self):
        """
        Make sure that locations aren't, and related data properly mapped to
        existing location instance.
        """
        strike_data = self.test_data['data']['strike'][1]
        strike_data['country'] = 'Yemen'
        strike_data['lat'] = '15.47467'
        strike_data['lon'] = '45.322755'

        self.country.delete()
        self.importer.data = self.test_data
        counter = self.importer.import_data()
        self.assertDictEqual(
            counter,
            {'locations': 1, 'strikes': 2, 'countries': 1, 'missing_coor': 0}
        )

        # Ensure that counters are correct.
        self.assertEqual(Strike.objects.count(), 2)
        Country.objects.get(), Location.objects.get()

    def test_import_data_invalid_data(self):
        """
        Make sure that data with invalid data is not imported to the database.
        """
        strike_data = self.test_data['data']['strike'][1]
        strike_data['lat'] = 'foobar'
        strike_data['country'] = 24
        strike_data['names'] = 666

        self.country.delete()
        self.importer.data = self.test_data
        counter = self.importer.import_data()
        self.assertDictEqual(
            counter,
            {'countries': 1, 'strikes': 1, 'missing_coor': 0, 'locations': 1}
        )

        # Ensure that counters are correct.
        country = Country.objects.get()
        location = Location.objects.get()
        strike = Strike.objects.get()
        self.assertEqual(country.name, 'Yemen')
        self.assertEqual(location.country, country)
        self.assertEqual(strike.location, location)


class LocationSerializerTest(BaseTestCase):
    """
    Unit tests for import data helper function.
    """

    def test_validate(self):
        """
        Ensure that only unique latitude and longitude combinations can be
        inserted into the database,
        """
        serializer = LocationSerializer()
        data = {'lat': '32.832865890', 'lon': '69.660186770'}
        return_data = serializer.validate(data)
        self.assertEqual(data, return_data)

        # Location exists.
        location = Location.objects.create(country=self.country, **data)
        with self.assertRaises(exceptions.ValidationError) as error:
            serializer.validate(data)
        self.assertEqual(
            str(error.exception.detail['error']), 'Location already exists.')
        self.assertEqual(
            str(error.exception.detail['instance']), str(location.id))


class LocationTest(BaseTestCase):
    """
    Unit tests for import data helper function.
    """

    def test_str(self):
        """
        Ensure proper str representation is returned.
        """
        location = Location.objects.create(country=self.country)
        self.assertEqual(str(location), '%d. SasaLand' % location.id)

        # Town str
        location.town = 'Gotham'
        location.save()
        self.assertEqual(str(location), '%d. SasaLand - Gotham' % location.id)

    def test_strike_info(self):
        """
        Returns a list or a dict, depending on a set of values related to the
        selected instance.
        """
        location = Location.objects.create(country=self.country)

        # No related strike
        self.assertEqual(location.strike_info, {})

        # One related strike
        Strike.objects.create(
            number=666,
            location=location,
            date=date(2002, 2, 1),
            articles=[],
            names=[],
            deaths='4'
        )
        strike_info = {
            'detail': True,
            'number': 666,
            'date': '02-01-2002',
            'deaths': '4'
        }
        self.assertDictEqual(location.strike_info, strike_info)

        # Multiple related strikes
        Strike.objects.create(
            number=777,
            location=location,
            date=date(2003, 3, 2),
            articles=[],
            names=[],
            deaths='3'
        )

        strike_info1 = {
            'number': 666,
            'date': '02-01-2002',
        }
        strike_info2 = {
            'number': 777,
            'date': '03-02-2003',
        }
        self.assertFalse(location.strike_info['detail'])
        self.assertEqual(location.strike_info['num_of_strikes'], 2)
        self.assertIn(strike_info1, location.strike_info['strikes'])
        self.assertIn(strike_info2, location.strike_info['strikes'])


class IndexViewTest(BaseTestCase):
    """
    Unit tests for import data helper function.
    """

    def setUp(self):
        super(IndexViewTest, self).setUp()
        self.view = IndexView()
        self.location = Location.objects.create(country=self.country)

    @freezegun.freeze_time('2012-01-14')
    def test_get(self):
        """
        Index GET,
        """
        strike = Strike.objects.create(
            number=666,
            location=self.location,
            date=date(2011, 10, 13),
            articles=[],
            names=[]
        )

        # Strike not in default range.
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['locations']), [])
        self.assertEqual(response.context['daterange'], '10-14-2011 - 01-14-2012')

        # Strike in default range.
        strike.date = date(2011, 10, 14)
        strike.save()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context['locations']), list(Location.objects.all()))
        self.assertEqual(response.context['daterange'], '10-14-2011 - 01-14-2012')

    @freezegun.freeze_time('2012-01-14')
    def test_date(self):
        """
        Date method responsible for parsing data for filtering.
        """
        date_range = {
            'date_lower': freezegun.api.FakeDate(2011, 10, 14),
            'date_upper': freezegun.api.FakeDate(2012, 1, 14)
        }
        self.assertEqual(self.view.date, date_range)
