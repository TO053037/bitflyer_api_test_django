import datetime

from django.test import TestCase
from .models import DayCandlesticks, HourCandlesticks
from .API import get_candle
from .indicator.sma import sma
from .Unix_time_and_datetime.convert_Unix_time import convert_datetime_to_unix_time, convert_unix_time_to_datetime


class DayCandlesticksTestCase(TestCase):
    def setUp(self):
        self.data = get_candle.get_candle_day()
        for candlestick in self.data:
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

    def test_exist_all_candle(self):
        for candle in self.data:
            close_time_unique_key = candle[0]
            self.assertEqual(1, DayCandlesticks.objects.filter(close_time=close_time_unique_key).count())

    def test_same_value_in_database(self):
        for candle in self.data:
            instance = DayCandlesticks.objects.get(close_time=candle[0])
            self.assertEqual(candle[0], instance.close_time)
            self.assertEqual(candle[1], instance.open_price)
            self.assertEqual(candle[2], instance.high_price)
            self.assertEqual(candle[3], instance.low_price)
            self.assertEqual(candle[4], instance.close_price)
            self.assertEqual(candle[5], instance.volume)
            self.assertEqual(candle[6], instance.quote_volume)


class HourCandlesticksTestCase(TestCase):
    def setUp(self):
        self.data = get_candle.get_candle_hour()
        print('setUp')
        for candlestick in self.data:
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

    def test_exist_all_candle(self):
        for candle in self.data:
            close_time_unique_key = candle[0]
            self.assertEqual(1, HourCandlesticks.objects.filter(close_time=close_time_unique_key).count())

    def test_same_value_in_database(self):
        for candle in self.data:
            instance = HourCandlesticks.objects.get(close_time=candle[0])
            self.assertEqual(candle[0], instance.close_time)
            self.assertEqual(candle[1], instance.open_price)
            self.assertEqual(candle[2], instance.high_price)
            self.assertEqual(candle[3], instance.low_price)
            self.assertEqual(candle[4], instance.close_price)
            self.assertEqual(candle[5], instance.volume)
            self.assertEqual(candle[6], instance.quote_volume)


class SMATestCase(TestCase):
    def setUp(self):
        for candlestick in get_candle.get_candle_day():
            try:
                DayCandlesticks.objects.get(close_time=candlestick[0])
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

    def test_sma(self):
        sma_list = [sma for sma in sma(datetime.datetime(year=2022, month=10, day=11), 3)]
        day1 = DayCandlesticks.objects.get(
            close_time=convert_datetime_to_unix_time(datetime.datetime(year=2022, month=10, day=11)))
        day2 = DayCandlesticks.objects.get(
            close_time=convert_datetime_to_unix_time(datetime.datetime(year=2022, month=10, day=10)))
        day3 = DayCandlesticks.objects.get(
            close_time=convert_datetime_to_unix_time(datetime.datetime(year=2022, month=10, day=9)))

        first_sma = (day1.close_price + day2.close_price + day3.close_price) / 3
        print(sma_list[:3])
        print(first_sma)
        self.assertEqual(sma_list[0], first_sma)
