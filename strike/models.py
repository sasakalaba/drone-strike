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
    lat = models.CharField(max_length=100)
    lon = models.CharField(max_length=100)
    # TODO: this should maybe be float
    # lat = models.DecimalField(max_digits=17, decimal_places=14, default='')
    # lon = models.DecimalField(max_digits=17, decimal_places=14, default='')
    country = models.CharField(max_length=100)
    town = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255)


    def __str__(self):
        return str(self.id)

    @property
    def coordinates(self):
        # TODO: return lat and lon as a dict
        return ''


# KADA POSTAVIS SVA POLJA PROVJERI KOJA MOGU BITI BLANK
#
