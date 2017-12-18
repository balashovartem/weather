from weather.observation.open_weather_map import OpenWeatherMap
from weather.observation.yandex_pogoda import YandexPogoda


def providers():
    """
    :return: array weather providers
    :rtype: Provider
    """
    return [OpenWeatherMap, YandexPogoda]
