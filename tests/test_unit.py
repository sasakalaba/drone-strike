# import os
from .base import BaseTestCase
from strike.helpers import Importer
# from decimal import Decimal, InvalidOperation
# from django.core.exceptions import ValidationError


class ImporterTest(BaseTestCase):
    """
    Unit tests for import data helper function.
    """

    def setUp(self):
        super(ImporterTest, self).setUp()
        self.importer = Importer()

    def test_parse_date(self):
        """
        Test for extracting proper date objects from date strings
        """
        pass

    def test_get_json(self):
        """
        Retrieves valid JSON data.
        """
        pass

    def test_import_data(self):
        """
        Imports data to the database.
        """
        pass
