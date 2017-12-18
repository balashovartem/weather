from django.test import TestCase
import weather.observation.provider as WP


class ProviderTestCase(TestCase):
    def test_yandex_pogoda(self):
        WP.YandexPogoda.temperature_at_city('tomsk')

    def test_yandex_pogoda_non_existent_city(self):
        with self.assertRaises(Exception):
            WP.YandexPogoda.temperature_at_city('123tomsk')

    def test_open_weather_map(self):
        WP.OpenWeatherMap.temperature_at_city('tomsk')

    def test_open_weather_map_non_existent_city(self):
        with self.assertRaises(Exception):
            WP.OpenWeatherMap.temperature_at_city('123tomsk')
