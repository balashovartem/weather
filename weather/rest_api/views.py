from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from rest_framework.decorators import list_route, api_view
from django_filters.rest_framework import DjangoFilterBackend
from weather.rest_api.serializers import WeatherSerializer
from weather.rest_api.models import Weather

from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

import weather.observation.provider as WP


class WeatherHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Weather history resource.
    """
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('location', 'timestamp')
    ordering = ('timestamp',)
    filter_fields = ('location',)

    @list_route()
    def last(self, request):
        self.queryset = Weather.objects.order_by('location', '-timestamp').distinct('location').all()
        self.filter_backends = (DjangoFilterBackend,)
        return self.list(request)


@api_view(['POST'])
def update_weather(request):
    json = JSONParser().parse(request.stream)
    for city in json['cities']:
        for provider in WP.providers():
            try:
                temperature, timestamp = provider.temperature_at_city(city)
                print(f'In city {city} temperature {temperature} .'
                      f' Data source {provider.source()}. Timestamp {timestamp}')
            except Exception as e:
                print(e)
    return Response(status=status.HTTP_400_BAD_REQUEST)
