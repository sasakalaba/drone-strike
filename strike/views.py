from django.http import HttpResponse
from django.template import loader
from .models import Strike


def index(request):
    template = loader.get_template('index.html')
    context = {'strikes': Strike.objects.all()}

    return HttpResponse(template.render(context, request))
