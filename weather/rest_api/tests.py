from django.test import TestCase
from django.test import Client
from weather.rest_api.models import Weather
from datetime import datetime
import pytz
import json


class WeatherTestCase(TestCase):
    def test_create_weather(self):
        city = 'city'
        timestamp = datetime.now(pytz.UTC)
        temperature = 25.5
        source = 'source'
        Weather.objects.create(city=city, temperature=temperature,
                               timestamp=timestamp, source=source)
        last_weather = Weather.objects.latest('id')
        self.assertEqual(last_weather.city, city)
        self.assertEqual(last_weather.timestamp, timestamp)
        self.assertEqual(last_weather.temperature, temperature)
        self.assertEqual(last_weather.source, source)

    def test_remove_weather(self):
        city = 'city'
        timestamp = datetime.now(pytz.UTC)
        temperature = 25.5
        source = 'source'
        Weather.objects.create(city=city, temperature=temperature,
                               timestamp=timestamp, source=source)
        last_weather = Weather.objects.latest('id')
        last_weather.delete()
        self.assertEqual(Weather.objects.all().count(), 0)

    def test_update_weather(self):
        city = 'city'
        timestamp = datetime.now(pytz.UTC)
        temperature = 25.5
        source = 'source'
        weather = Weather.objects.create(city=city, temperature=temperature,
                                         timestamp=timestamp, source=source)
        city = 'city1'
        timestamp = datetime.now(pytz.UTC)
        temperature = 20
        source = 'source1'
        weather.city = city
        weather.timestamp = timestamp
        weather.temperature = temperature
        weather.source = source
        weather.save()

        last_weather = Weather.objects.latest('id')
        self.assertEqual(last_weather.city, last_weather.city)
        self.assertEqual(last_weather.timestamp, last_weather.timestamp)
        self.assertEqual(last_weather.temperature, last_weather.temperature)
        self.assertEqual(last_weather.source, last_weather.source)


class ViewTestCase(TestCase):
    def test_weather_history_empty(self):
        c = Client()
        response = c.get('/weather_history/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '[]')

    def test_weather_history_not_empty(self):
        weather = Weather.objects.create(city='city', temperature=25.5,
                                         timestamp=datetime.now(pytz.UTC), source='source')
        c = Client()
        response = c.get('/weather_history/')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(len(json_response), 1)
        self.assertEqual(json_response[0]['city'], weather.city)
        self.assertEqual(json_response[0]['temperature'], weather.temperature)
        json_timestamp = datetime.strptime(json_response[0]['timestamp'],
                                           '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=pytz.UTC)
        self.assertEqual(json_timestamp, weather.timestamp)
        self.assertEqual(json_response[0]['source'], weather.source)

    def test_weather_history_last_empty(self):
        c = Client()
        response = c.get('/weather_history/last/')
        self.assertEqual(response.status_code, 404)

    def test_weather_history_last_not_empty(self):
        weather = Weather.objects.create(city='city', temperature=25.5,
                                         timestamp=datetime.now(pytz.UTC), source='source')
        c = Client()
        response = c.get('/weather_history/last/?city=city')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(len(json_response), 1)
        self.assertEqual(json_response[0]['city'], weather.city)
        self.assertEqual(json_response[0]['temperature'], weather.temperature)
        json_timestamp = datetime.strptime(json_response[0]['timestamp'],
                                           '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=pytz.UTC)
        self.assertEqual(json_timestamp, weather.timestamp)
        self.assertEqual(json_response[0]['source'], weather.source)

    def test_weather_history_last_not_empty_wrong_city(self):
        Weather.objects.create(city='city', temperature=25.5,
                               timestamp=datetime.now(pytz.UTC), source='source')
        c = Client()
        response = c.get('/weather_history/last/?city=city123')
        self.assertEqual(response.status_code, 404)

    def test_update_weather(self):
        c = Client()
        response = c.post('/update_weather', data=json.dumps({'cities': ['tomsk']}),
                          content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_update_weather_empty_cities(self):
        c = Client()
        response = c.post('/update_weather', data=json.dumps({'cities': []}),
                          content_type='application/json')
        self.assertEqual(response.status_code, 200)
