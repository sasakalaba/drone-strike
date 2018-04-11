from datetime import datetime
from dateutil.relativedelta import relativedelta
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
            'date_lower': (today - relativedelta(months=300)).date(),
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

        self.context = {
            'locations': locations,
            'daterange': ' - '.join([
                self.date['date_lower'].strftime("%m-%d-%Y"),
                self.date['date_upper'].strftime("%m-%d-%Y")
            ])
        }
        return render(request, self.template, self.context)
