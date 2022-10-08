from django.test import TestCase
from .models import DayCandlesticks
from .API import get_candle


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
