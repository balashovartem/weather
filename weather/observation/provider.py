import abc
from http.client import HTTPConnection, HTTPSConnection
import json
from datetime import datetime
from lxml import html
import dateparser


class Provider:
    @classmethod
    @abc.abstractclassmethod
    def source(cls):
        """
        :return: Name of weather provider
        :rtype: str
        """
        ...

    @classmethod
    @abc.abstractclassmethod
    def temperature_at_city(cls, city):
        """
        :return: (temperature in celsius at city, timestamp)
        :rtype: (float, datetime)
        """
        ...


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


class YandexPogoda(Provider):
    """
    yandex.ru/pogoda weather provider
    """
    @classmethod
    def source(cls):
        return 'yandex_pogoda'

    @classmethod
    def temperature_at_city(cls, city):
        if not city:
            raise ValueError("city is empty")
        connection = HTTPSConnection('yandex.ru', 443)
        url = f'/pogoda/{city}'
        connection.request('GET', url)
        response = connection.getresponse()
        if response.code != 200:
            raise RuntimeError(f'yandex.ru{url} {response.code} {response.reason}')
        timestamp = dateparser.parse(response.headers['date'])
        data = response.read()
        tree = html.document_fromstring(data)
        span_text = tree.xpath('/html/body/div[3]/div[1]/div[1]/div[2]/div[1]/a/div/span[1]/text()')[0]
        temperature = span_text.replace('−', '-')
        return float(temperature), timestamp


def providers():
    """
    :return: array weather providers
    :rtype: Provider
    """
    return [OpenWeatherMap, YandexPogoda]
