from django.test import TestCase
from .models import HourCandlesticks
from .API import get_candle


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
