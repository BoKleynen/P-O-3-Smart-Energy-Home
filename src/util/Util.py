from datetime import datetime, date, time, timedelta
from typing import Generator


def time_range(start: time=time(0, 0), end: time=time(23, 59)) -> Generator[time, time, None]:
    start_datetime = datetime(2017, 1, 1, hour=start.hour, minute=start.minute)
    for i in range(0, (end.hour*60 + end.minute) - (start.hour*60 + start.minute), 5):
        yield (start_datetime + timedelta(minutes=i)).time()


def date_range(start: date, end: date):
    for i in range((end - start).days):
        yield start + timedelta(days=i)


def datetime_range(start: datetime, end: datetime, delta: timedelta):
    t = start
    while t <= end:
        yield t
        t += delta
