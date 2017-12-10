from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from rest_framework.decorators import list_route
from django_filters.rest_framework import DjangoFilterBackend
from weather.rest_api.serializers import WeatherSerializer
from weather.rest_api.models import Weather


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
        self.queryset = Weather.objects.order_by('location','-timestamp').distinct('location').all()
        self.filter_backends = (DjangoFilterBackend,)
        return self.list(request)

