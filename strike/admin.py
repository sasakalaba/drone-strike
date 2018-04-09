from django.contrib import admin
from .models import Strike, Location


class StrikeInline(admin.TabularInline):
    model = Strike
    fields = ('deaths', 'date')


class LocationAdmin(admin.ModelAdmin):
    model = Location
    list_display = [
        'country',
    ]
    list_filter = ()
    inlines = [StrikeInline, ]


class StrikeAdmin(admin.ModelAdmin):
    model = Strike
    list_display = [
        'number',
    ]
    list_filter = ()


admin.site.register(Strike, StrikeAdmin)
admin.site.register(Location, LocationAdmin)
