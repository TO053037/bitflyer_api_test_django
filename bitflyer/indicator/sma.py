import datetime
from typing import List, Generator

from ..Unix_time_and_datetime.convert_Unix_time import convert_datetime_to_unix_time
from ..models import DayCandlesticks
from .cal_average import cal_average


def sma(base_datetime: datetime.datetime, period: int) -> Generator[float, None, None]:
    is_exist_data = True
    while is_exist_data:
        close_price_list = []
        for day in range(period):
            try:
                close_price_list.append(
                    DayCandlesticks.objects.get(
                        close_time=convert_datetime_to_unix_time(
                            base_datetime - datetime.timedelta(days=day))).close_price
                )
            except DayCandlesticks.DoesNotExist:
                is_exist_data = False
                break

        if len(close_price_list) == period:
            yield cal_average(close_price_list)

        base_datetime -= datetime.timedelta(days=1)
