from django.http import HttpResponse
from django.template import loader
from .models import Location


def index(request):
    template = loader.get_template('index.html')
    # template = loader.get_template('test_map.html')

    # locations = Location.objects.all()
    locations = Location.objects.exclude(lat__exact='', lon__exact='')
    context = {'locations': locations}

    return HttpResponse(template.render(context, request))
