import datetime


def convert_unix_time_to_datetime(unix_time: int) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(unix_time)


def convert_datetime_to_unix_time(datetime: datetime.datetime) -> float:
    return datetime.timestamp()
