from weather.rest_api.models import Weather
from rest_framework import serializers


class WeatherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Weather
        fields = ('id', 'city', 'source', 'temperature', 'timestamp')


class ErrorSerializer(serializers.Serializer):
    city = serializers.CharField()
    source = serializers.CharField()
    error = serializers.CharField()
