from django.test import TestCase
from strike.models import Country



class BaseTestCase(TestCase):
    """
    Base test class.
    """

    def setUp(self):
        self.country = Country.objects.create(name='SasaLand')
