from django.db import models


class Weather(models.Model):
    city = models.CharField(max_length=168, db_index=True, blank=False)
    source = models.CharField(max_length=30, blank=False)
    temperature = models.FloatField(blank=False)
    timestamp = models.DateTimeField(db_index=True, blank=False)
