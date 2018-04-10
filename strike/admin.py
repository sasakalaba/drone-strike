from django.contrib import admin
from .models import Strike, Location, Country


class StrikeInline(admin.TabularInline):
    model = Strike
    fields = ('deaths', 'date')


class LocationAdmin(admin.ModelAdmin):
    model = Location
    list_display = ['id', 'country', 'town', 'location']
    list_filter = ('country', )
    inlines = [StrikeInline, ]


class StrikeAdmin(admin.ModelAdmin):
    model = Strike
    list_display = ['location', 'date', 'deaths']
    list_filter = ('location__country', )


class CountryAdmin(admin.ModelAdmin):
    model = Country
    list_display = ['name', ]


admin.site.register(Strike, StrikeAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Country, CountryAdmin)
