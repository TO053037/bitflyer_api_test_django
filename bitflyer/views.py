import datetime

from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render
import pybitflyer
from .models import DayCandlesticks, HourCandlesticks
from .API import get_candle
from .Unix_time_and_datetime.convert_Unix_time import convert_datetime_to_unix_time
from .indicator.sma import sma


def index(request: HttpRequest):
    response = pybitflyer.API().ticker(product_code='BTC_JPY')
    for k, v in response.items():
        print(k, v)
    return render(request, 'bitflyer/index.html', response)


def save_data(request: HttpRequest):
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

    for candlestick in get_candle.get_candle_hour():
        try:
            HourCandlesticks.objects.get(close_time=candlestick[0])
            print('duplicate')
        except HourCandlesticks.DoesNotExist:
            instance_hour_candlesticks = HourCandlesticks()
            instance_hour_candlesticks.close_time = candlestick[0]
            instance_hour_candlesticks.open_price = candlestick[1]
            instance_hour_candlesticks.high_price = candlestick[2]
            instance_hour_candlesticks.low_price = candlestick[3]
            instance_hour_candlesticks.close_price = candlestick[4]
            instance_hour_candlesticks.volume = candlestick[5]
            instance_hour_candlesticks.quote_volume = candlestick[6]
            instance_hour_candlesticks.save()

    return render(request, 'bitflyer/index.html')


def get_candlesticks(request: HttpRequest) -> JsonResponse:
    day_period = int(request.GET.get('day_period'))
    today = datetime.datetime.now()
    date = datetime.datetime(year=today.year, month=today.month, day=today.day - 1, hour=0, minute=0, second=0)
    candlesticks = [[0 for _ in range(5)] for _ in range(day_period)]
    for i in reversed(range(day_period)):
        try:
            instance_day_candlesticks = DayCandlesticks.objects.get(close_time=convert_datetime_to_unix_time(date))
        except DayCandlesticks.DoesNotExist:
            return JsonResponse({
                'status': 400
            })

        candlesticks[i][0] = date
        candlesticks[i][1] = instance_day_candlesticks.low_price
        candlesticks[i][2] = instance_day_candlesticks.open_price
        candlesticks[i][3] = instance_day_candlesticks.close_price
        candlesticks[i][4] = instance_day_candlesticks.high_price
        date -= datetime.timedelta(days=1)

    for candlestick in candlesticks:
        print(candlestick)

    return JsonResponse({
        'status': 200,
        'candlesticks': candlesticks,
    })


def get_sma(request: HttpRequest) -> JsonResponse:
    day_period = int(request.GET.get('day_period'))
    today = datetime.datetime.now()
    base_datetime = datetime.datetime(year=today.year, month=today.month, day=today.day - 1)
    return JsonResponse({
        'status': 200,
        'sma_list': [s for s in sma(base_datetime, day_period)],
    })
