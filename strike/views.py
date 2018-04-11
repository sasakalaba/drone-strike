from django.shortcuts import render
from django.views import View
from .models import Location


class Index(View):
    template = 'index.html'
    context = {}

    def get(self, request, *args, **kwargs):
        locations = Location.objects.all()
        self.context = {'locations': locations}
        return render(request, self.template, self.context)
