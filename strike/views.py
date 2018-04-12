from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.shortcuts import render
from django.views import View
from .models import Strike, Location


class IndexView(View):
    template = 'index.html'
    context = {}

    @property
    def date(self):
        """
        Helper method for handling view related dates.
        """
        today = datetime.today()
        return {
            'date_lower': (today - relativedelta(
                months=settings.STRIKE_DATE_MONTH_RANGE)).date(),
            'date_upper': today.date(),
        }

    def get(self, request, *args, **kwargs):
        """
        Main view.
        """
        # Get strikes from last 3 months by default.ž
        locations_ids = Strike.objects.filter(
            date__gte=self.date['date_lower'],
            date__lte=self.date['date_upper']
        ).values_list('location_id', flat=True).distinct()

        locations = Location.objects.filter(id__in=locations_ids)

        # Set filter values for selected locations
        city_filters = {}
        province_filters = {}

        country_filters = locations.values_list('country__name', flat=True).distinct()
        for country in country_filters:
            city_filters[country] = locations.filter(
                country__name=country).values_list('town', flat=True).distinct()
            province_filters[country] = locations.filter(
                country__name=country).values_list('location', flat=True).distinct()

        self.context = {
            'locations': locations,
            'daterange': ' - '.join([
                self.date['date_lower'].strftime("%m-%d-%Y"),
                self.date['date_upper'].strftime("%m-%d-%Y")
            ]),
            'country_filters': country_filters,
            'city_filters': city_filters,
            'province_filters': province_filters
        }
        return render(request, self.template, self.context)
