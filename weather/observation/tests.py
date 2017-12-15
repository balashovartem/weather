from django.test import TestCase
import weather.observation.provider as WP


class ProviderTestCase(TestCase):
    def test_yandex_pogoda(self):
        WP.YandexPogoda.temperature_at_city('tomsk')

    def test_open_weather_map(self):
        WP.OpenWeatherMap.temperature_at_city('tomsk')
