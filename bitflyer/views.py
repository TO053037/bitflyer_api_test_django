from django.http import HttpResponse
from django.shortcuts import render, redirect
import pybitflyer
from .models import DayCandlesticks
from .API import get_candle


def index(request: HttpResponse):
    response = pybitflyer.API().ticker(product_code='BTC_JPY')
    for k, v in response.items():
        print(k, v)
    return render(request, 'bitflyer/index.html', response)


def save_data(request: HttpResponse):
    for candlestick in get_candle.get_candle_day():
        try:
            DayCandlesticks.objects.get(close_time=candlestick[0])
            print('duplicate')
        except DayCandlesticks.DoesNotExist:
            instance_day_candlesticks = DayCandlesticks()
            instance_day_candlesticks.close_time = candlestick[0]
            instance_day_candlesticks.open_price = candlestick[1]
            instance_day_candlesticks.high_price = candlestick[2]
            instance_day_candlesticks.low_price = candlestick[3]
            instance_day_candlesticks.close_price = candlestick[4]
            instance_day_candlesticks.volume = candlestick[5]
            instance_day_candlesticks.quote_volume = candlestick[6]
            instance_day_candlesticks.save()
    return render(request, 'bitflyer/index.html')
