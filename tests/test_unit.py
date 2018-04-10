import mock
import json
from datetime import date
from django.core.exceptions import ValidationError
from strike.helpers import Importer
from strike.models import Location, Country
from strike.serializers import LocationSerializer
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

            def read(self):
                raise json.JSONDecodeError(msg='', doc=Doc(), pos=3)

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
        get_json bad request.
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
        get_json bad request.
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

    def test_ostatak(self):
        """
        Test ostatak metode i refaktoraj.
        """
        pass


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
        data = {'lat': '32.832865890',  'lon': '69.660186770'}
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
        self.assertEqual(str(location), 'SasaLand')

        # Town str
        location.town = 'Gotham'
        location.save()
        self.assertEqual(str(location), 'SasaLand - Gotham')
