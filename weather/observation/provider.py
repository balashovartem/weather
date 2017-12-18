import abc


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
