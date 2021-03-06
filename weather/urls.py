from django.conf.urls import url, include
from rest_framework import routers
from weather.rest_api import views

router = routers.DefaultRouter()
router.register(r'weather_history', views.WeatherHistoryViewSet)
router.register(r'last_weather_history', views.LastWeatherHistoryViewSet, "last")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'update_weather', views.update_weather),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
