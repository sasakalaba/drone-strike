from datetime import datetime
from django import forms
from .models import Location


class StrikeFilterForm(forms.Form):
    daterange = forms.CharField(label='Date', max_length=23)
    country__name = forms.ChoiceField(label='Country', choices=())
    province = forms.CharField(label='Province', max_length=100, required=False)
    town = forms.CharField(label='City / Town', max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super(StrikeFilterForm, self).__init__(*args, **kwargs)
        country_choices = [
            (l, l) for l in Location.objects.all().values_list(
                'country__name', flat=True).distinct()]
        country_choices.append(('all', ''))
        self.fields['country__name'] = forms.ChoiceField(choices=country_choices)

    def get_values(self):
        """
        Get filter unpackable values.
        """
        if not self.is_valid():
            return {}

        # Only retrieve existing data.
        data = {}
        for item in self.cleaned_data:
            if self.cleaned_data[item] not in ['', None]:
                data[item] = self.cleaned_data[item]

        # Set province key
        if 'province' in data:
            data['location'] = data.pop('province')

        # Set country default value
        if data.get('country__name', '') == 'all':
            data.pop('country__name')

        return data

    def clean_daterange(self):
        """
        Parses and validates daterange string.
        """
        error = forms.ValidationError("Date range must be 'mm/dd/yyyy - mm/dd/yyyy'.")

        if not self.is_valid():
            raise error

        daterange = self.cleaned_data['daterange']
        dates = daterange.split(' - ')
        if len(dates) != 2:
            raise error

        try:
            daterange = {
                'date__gte': datetime.strptime(dates[0], '%m/%d/%Y').date(),
                'date__lte': datetime.strptime(dates[1], '%m/%d/%Y').date(),
            }
        except ValueError:
            raise error

        return daterange
