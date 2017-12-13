from django.db import models


class Weather(models.Model):
    city = models.CharField(max_length=168, db_index=True)
    source = models.CharField(max_length=30)
    temperature = models.FloatField()
    timestamp = models.DateTimeField(db_index=True)
