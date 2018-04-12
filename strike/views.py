from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render
from django.views import View
from .forms import StrikeFilterForm
from .models import Strike, Location


class IndexView(View):
    template = 'index.html'
    context = {}

    @property
    def default_daterange(self):
        """
        Helper method for handling view related dates.
        """
        today = datetime.today()
        return {
            'date__gte': (today - relativedelta(
                months=settings.STRIKE_DATE_MONTH_RANGE)).date(),
            'date__lte': today.date(),
        }

    def get(self, request, *args, **kwargs):
        """
        Main view.
        """
        form = StrikeFilterForm(data=request.GET)
        filter_params = {}
        daterange = None

        if form.is_valid():
            filter_params = form.get_values()

            # Get unique strikes for the desired daterange.
            daterange = filter_params.pop('daterange')
            location_ids = Strike.objects.filter(
                **daterange).values_list('location_id', flat=True).distinct()

        else:
            # Get unique strikes from last 3 months by default.
            location_ids = Strike.objects.filter(
                **self.default_daterange).values_list('location_id', flat=True).distinct()
            self.context['form_errors'] = form.errors

        locations = Location.objects.filter(id__in=location_ids, **filter_params)

        # Set filter values for selected locations
        city_filters = {}
        province_filters = {}

        country_filters = Location.objects.all().values_list(
            'country__name', flat=True).distinct()
        for country in country_filters:
            city_filters[country] = Location.objects.all().filter(
                country__name=country).values_list('town', flat=True).distinct()
            province_filters[country] = Location.objects.all().filter(
                country__name=country).values_list('location', flat=True).distinct()

        # Return last valid daterange
        if daterange:
            daterange_str = ' - '.join([
                daterange['date__gte'].strftime("%m-%d-%Y"),
                daterange['date__lte'].strftime("%m-%d-%Y")
            ])
        else:
            daterange_str = ' - '.join([
                self.default_daterange['date__gte'].strftime("%m-%d-%Y"),
                self.default_daterange['date__lte'].strftime("%m-%d-%Y")
            ])

        self.context = {
            'locations': locations,
            'daterange': daterange_str,
            'country_filters': country_filters,
            'city_filters': city_filters,
            'province_filters': province_filters,
            'form': form
        }
        return render(request, self.template, self.context)


class SearchView(View):
    template = 'index.html'
    context = {}
    text_fields = (
        'narrative', 'deaths', 'deaths_min', 'deaths_max', 'civilians',
        'injuries', 'children', 'tweet_id', 'bureau_id', 'bij_summary_short',
        'target', 'articles', 'names', 'location__country__name', 'location__town',
        'location__location'
    )


    def get(self, request, *args, **kwargs):
        """
        Search view.
        """
        query = request.GET.get('search_q', '')
        queries = []

        if query:
            for field in self.text_fields:
                queries.append(Q(**{field + '__icontains': query}))

            final_query = queries.pop()
            for item in queries:
                final_query |= item

            strikes = Strike.objects.filter(final_query)
            location_ids = strikes.values_list('location_id', flat=True).distinct()
            locations = Location.objects.filter(id__in=location_ids)

        self.context = {
            'query': query,
            'strikes': strikes,
            'locations': locations,
        }
        return render(request, self.template, self.context)
