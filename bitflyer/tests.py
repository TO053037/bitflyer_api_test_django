from django.test import TestCase
from .Unix_time_and_datetime.convert_Unix_time import convert_unix_time_to_datetime
import datetime


class ConvertUnixTimeToDateTimeTestCase(TestCase):
    def test_convert_unix_time_to_datetime(self):
        print('test_convert_unix_time_to_datetime')
        self.assertEqual(convert_unix_time_to_datetime(0),
                         datetime.datetime(year=1970, month=1, day=1, hour=0, minute=0, second=0))
        self.assertEqual(convert_unix_time_to_datetime(1474732800),
                         datetime.datetime(year=2016, month=9, day=24, hour=16, minute=0, second=0))
        self.assertEqual(convert_unix_time_to_datetime(1474736400),
                         datetime.datetime(year=2016, month=9, day=24, hour=17, minute=0, second=0))
