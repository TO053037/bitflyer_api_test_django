from typing import List

import requests

URL = 'https://api.cryptowat.ch/markets/bitflyer/btcjpy/ohlc'


def get_candle_day() -> List[List[float]]:
    response = requests.get(URL + '?periods=86400&after=1617202800').json()
    return response['result']['86400']


def get_candle_hour() -> List[List[float]]:
    response = requests.get(URL + '?periods=3600&after=1631718000').json()
    return response['result']['3600']
