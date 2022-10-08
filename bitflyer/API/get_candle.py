from typing import List

import requests
URL = 'https://api.cryptowat.ch/markets/bitflyer/btcjpy/ohlc'


def get_candle_day() -> List[List[float]]:
    day = "?periods=86400&after=1617202800"
    response = requests.get(URL + day).json()
    return response['result']['86400']

