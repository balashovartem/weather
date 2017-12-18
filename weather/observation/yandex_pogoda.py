from weather.observation.provider import Provider
from http.client import HTTPSConnection
import dateparser
from lxml import html


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
