from django.conf import settings


def google_key(request):
    return {'GOOGLE_MAPS_JS_API_KEY': settings.GOOGLE_MAPS_JS_API_KEY}
