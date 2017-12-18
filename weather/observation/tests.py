from django.test import TestCase
from parameterized import parameterized, param
from weather.observation.open_weather_map import OpenWeatherMap
from weather.observation.yandex_pogoda import YandexPogoda


class ProviderTestCase(TestCase):
    @parameterized.expand([
        param(OpenWeatherMap),
        param(YandexPogoda)
    ])
    def test_provider_temperature(self, provider):
        provider.temperature_at_city('tomsk')

    @parameterized.expand([
        param(OpenWeatherMap),
        param(YandexPogoda)
    ])
    def test_provider_temperature_non_existent_city(self, provider):
        with self.assertRaises(Exception):
            provider.temperature_at_city('123tomsk')
