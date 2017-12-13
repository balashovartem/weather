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
    ordering_fields = ('city', 'timestamp')
    ordering = ('timestamp',)
    filter_fields = ('city',)

    @list_route()
    def last(self, request):
        self.queryset = Weather.objects.order_by('city', '-timestamp').distinct('city').all()
        self.filter_backends = (DjangoFilterBackend,)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        if not len(queryset):
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)


@api_view(['POST'])
def update_weather(request):
    json_request = JSONParser().parse(request.stream)
    json_error_response = []
    for city in json_request['cities']:
        for provider in WP.providers():
            try:
                temperature, timestamp = provider.temperature_at_city(city)
                Weather.objects.create(city=city, temperature=temperature,
                                       timestamp=timestamp, source=provider.source())
            except Exception as e:
                json_error_response.append({'source': provider.source(), 'error': str(e)})
    if len(json_error_response) > 0:
        return Response(json_error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status=status.HTTP_200_OK)
