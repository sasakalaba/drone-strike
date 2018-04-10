from django.contrib.postgres.fields import ArrayField
from django.db import models


class Strike(models.Model):
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(unique=True)
    date = models.DateField(default=None)
    narrative = models.TextField(blank=True, null=True)
    deaths = models.CharField(max_length=50, blank=True, null=True)
    deaths_min = models.CharField(max_length=50, blank=True, null=True)
    deaths_max = models.CharField(max_length=50, blank=True, null=True)
    civilians = models.CharField(max_length=1000, blank=True, null=True)
    injuries = models.CharField(max_length=1000, blank=True, null=True)
    children = models.CharField(max_length=1000, blank=True, null=True)
    tweet_id = models.CharField(max_length=18)
    bureau_id = models.CharField(max_length=10)
    bij_summary_short = models.CharField(max_length=1000, blank=True, null=True)
    bij_link = models.URLField(max_length=300)
    target = models.CharField(max_length=1000, blank=True, null=True)
    articles = ArrayField(models.CharField(max_length=255, blank=True))
    names = ArrayField(models.CharField(max_length=10000000, blank=True))

    def __str__(self):
        return str(self.number)


class Location(models.Model):
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    lat = models.CharField(max_length=100)
    lon = models.CharField(max_length=100)
    # TODO: this should maybe be float
    # lat = models.DecimalField(max_digits=17, decimal_places=14, default='')
    # lon = models.DecimalField(max_digits=17, decimal_places=14, default='')
    town = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255)


    def __str__(self):
        if self.town:
            return ' - '.join([self.country.name, self.town])
        return self.country.name

    @property
    def coordinates(self):
        # TODO: return lat and lon as a dict
        return ''


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return str(self.name)
