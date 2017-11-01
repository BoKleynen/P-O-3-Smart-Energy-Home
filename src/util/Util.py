from datetime import datetime, date, time, timedelta
from typing import Generator


def time_range(start: time, end: time) -> Generator[time, time, None]:
    start_datetime = datetime(2017, 1, 1, hour=start.hour, minute=start.minute)
    for i in range((end.hour*60 + end.minute) - (start.hour*60 + start.minute)):
        yield (start_datetime + timedelta(minutes=i)).time()


def date_range(start: date, end: date):
    for i in range ((end - start).days):
        yield start + timedelta(days=i)