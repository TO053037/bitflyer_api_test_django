from typing import List


def cal_average(price_list: List[float]) -> float:
    result = 0.0
    for price in price_list:
        result += price
    return result / len(price_list)

