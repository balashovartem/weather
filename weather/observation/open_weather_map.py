from weather.observation.provider import Provider
from http.client import HTTPConnection
import dateparser
import json


class OpenWeatherMap(Provider):
    """
    openweathermap.org weather provider
    """
    appid = '84294b9e4fa900829ea3ad3bc4947527'

    @classmethod
    def source(cls):
        return 'open_weather_map'

    @classmethod
    def temperature_at_city(cls, city):
        if not city:
            raise ValueError("city is empty")
        connection = HTTPConnection('api.openweathermap.org', 80)
        url = f'/data/2.5/find?q={city}&units=metric&APPID={cls.appid}'
        connection.request('GET', url)
        response = connection.getresponse()
        if response.code != 200:
            raise RuntimeError(f'api.openweathermap.org{url} {response.code} {response.reason}')
        timestamp = dateparser.parse(response.headers['date'])
        data = response.read()
        json_object = json.loads(data)
        return float(json_object['list'][0]['main']['temp']), timestamp
