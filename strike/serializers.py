from rest_framework import serializers
from .models import Strike, Location


class StrikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Strike
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

    def validate(self, data):
        """
        Custom validation for uniqueness of lat and lon.
        """
        # TODO: Replace this with GeoDjango PointField.
        #       https://trello.com/c/03yB0K0n
        if data['lat'] and data['lon']:
            try:
                location = Location.objects.get(lat=data['lat'], lon=data['lon'])
                raise serializers.ValidationError({
                    'error': 'Location already exists.',
                    'instance': location.id
                })
            except Location.DoesNotExist:
                pass

        return data
