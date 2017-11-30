from abc import ABCMeta
from typing import Callable
import pandas as pd

class Load(metaclass=ABCMeta):
    """
    Base class for modelling all the loads in a house

    power consumption should be expressed in kW (= 1000W)
    time in seconds and relative to 00:00 when expressing a time of the day
    """

    def __init__(self, power_consumption: Callable):
        """

        :param power_consumption:
        """
        self._power_consumption = power_consumption

    @property
    def power_consumption(self):
        return self._power_consumption


class ContinuousLoad(Load):
    """
    Model for loads that have a relatively constant drain throughout the day.

    e.g.: freezer, fridge, ...
    """

    def __init__(self, power_consumption: Callable[[float], float]):
        super().__init__(power_consumption)


class CyclicalLoad(Load, metaclass=ABCMeta):
    def __init__(self, power_consumption, execution_date: pd.Timestamp, start_time: pd.Timestamp, cycle_duration: float,
                 time_delta: pd.DateOffset):
        super().__init__(power_consumption)
        self._execution_date = execution_date
        self._start_time = start_time
        self._cycle_duration = cycle_duration
        self._time_delta = time_delta

    @property
    def start_timestamp(self) -> pd.Timestamp:
        return datetime.combine(self._execution_date, self._start_time)

    @property
    def execution_date(self) -> date:
        return self._execution_date

    @property
    def start_time(self) -> float:
        return 3600*self.start_timestamp.time().hour \
               + 60*self.start_timestamp.time().minute \
               + self.start_timestamp.time().second

    @property
    def time_delta(self) -> timedelta:
        return self._time_delta

    @property
    def cycle_duration(self) -> float:
        return self._cycle_duration


class TimedLoad(CyclicalLoad):
    """
    Model for loads that have a relatively fixed start time and duration

    e.g.: cooking, watching television, ...
    """

    def __init__(self, power_consumption: Callable[[float], float], execution_date: date, start_time: time,
                 cycle_duration: float, time_delta: timedelta):
        """

        :param power_consumption: A function taking one argument (of time) that describes the power consumption of this
        load, assumed to be zero outside of [self.start_time, self.start_time + self.cycle_duration].
        :param start_time:
        :param cycle_duration:
        """
        super().__init__(power_consumption, execution_date, start_time, cycle_duration, time_delta)


class StaggeredLoad(CyclicalLoad):
    """
    Model for loads that can be freely moved throughout a day by and optimisation algorithm.

    e.g.: dishwasher, washing machine , ...
    """

    def __init__(self, power_consumption: Callable[[float], float], execution_date: date, original_start_time,
                 cycle_duration: float, due_time: time, time_delta: timedelta):
        super().__init__(power_consumption, execution_date, original_start_time, cycle_duration, time_delta)
        self._due_time = due_time
        self._original_start_time = original_start_time

    @property
    def due_time(self):
        return self._due_time

    @property
    def original_start_time(self):
        return self._original_start_time

    def set_start_time(self, start_time: time):
        super()._start_time = start_time
