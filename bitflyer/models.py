from django.db import models


class DayCandlesticks(models.Model):
    close_time = models.FloatField(unique=True)
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField(default=0.0)
    volume = models.FloatField()
    quote_volume = models.FloatField()
