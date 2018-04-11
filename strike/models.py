from django.contrib.postgres.fields import ArrayField
from django.db import models


class Strike(models.Model):
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(unique=True)
    date = models.DateField(default=None)
    narrative = models.TextField(max_length=1000, blank=True, null=True)
    deaths = models.CharField(max_length=50, blank=True, null=True)
    deaths_min = models.CharField(max_length=50, blank=True, null=True)
    deaths_max = models.CharField(max_length=50, blank=True, null=True)
    civilians = models.CharField(max_length=50, blank=True, null=True)
    injuries = models.CharField(max_length=50, blank=True, null=True)
    children = models.CharField(max_length=50, blank=True, null=True)
    tweet_id = models.CharField(max_length=18, blank=True, null=True)
    bureau_id = models.CharField(max_length=10, blank=True, null=True)
    bij_summary_short = models.TextField(max_length=1000, blank=True, null=True)
    bij_link = models.URLField(max_length=300, blank=True, null=True)
    target = models.CharField(max_length=1000, blank=True, null=True)
    articles = ArrayField(models.CharField(max_length=255, blank=True))
    names = ArrayField(models.CharField(max_length=10000000, blank=True))

    def __str__(self):
        return str(self.number)


class Location(models.Model):
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    lat = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    lon = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    town = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        if self.town:
            return ' - '.join([self.country.name, self.town])
        return self.country.name


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return str(self.name)
