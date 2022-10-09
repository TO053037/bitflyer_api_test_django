import datetime


def convert_unix_time_to_datetime(unix_time: int) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(unix_time)
