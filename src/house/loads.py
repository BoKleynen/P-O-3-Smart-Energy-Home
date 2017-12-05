from abc import ABCMeta
from datetime import date, time
import pandas as pd
from datetime import date


class Load(metaclass=ABCMeta):
    """
    Base class for modelling all the loads in a house

    power consumption should be expressed in kW (= 1000W)
    time in seconds and relative to 00:00 when expressing a time of the day
    """

    def __init__(self, power_consumption: float):
        """

        :param power_consumption:
        """
        self._power_consumption = power_consumption

    @property
    def power_consumption(self) -> float:
        return self._power_consumption


class ContinuousLoad(Load):
    """
    Model for loads that have a relatively constant drain throughout the day.

    e.g.: freezer, fridge, ...
    """

    def __init__(self, power_consumption: float):
        super().__init__(power_consumption)


class CyclicalLoad(Load, metaclass=ABCMeta):
    def __init__(self, power_consumption: float, start_time: time, cycle_duration: float,
                 time_delta: pd.DateOffset, execution_date: date=None):

        super().__init__(power_consumption)

        self._execution_date = execution_date
        self._start_time = start_time
        self._cycle_duration = cycle_duration
        self._time_delta = time_delta

    @property
    def execution_date(self) -> date:
        return self._execution_date

    @execution_date.setter
    def execution_date(self, execution_date: date):
        self._execution_date = execution_date

    @property
    def start_time(self) -> float:
        return 3600*self._start_time.hour + 60*self._start_time.minute + self._start_time.second

    @start_time.setter
    def start_time(self, start_time: time):
        self._start_time = start_time

    @property
    def start_timestamp(self) -> pd.Timestamp:
        return pd.Timestamp.combine(self._execution_date, self._start_time)

    @property
    def time_delta(self) -> pd.DateOffset:
        return self._time_delta

    @property
    def cycle_duration(self) -> float:
        return self._cycle_duration


class TimedLoad(CyclicalLoad):
    """
    Model for loads that have a relatively fixed start time and duration

    e.g.: cooking, watching television, ...
    """

    def __init__(self, power_consumption: float, start_time: time,
                 cycle_duration: float, time_delta: pd.DateOffset, execution_date: date=None):

        super().__init__(power_consumption, start_time, cycle_duration, time_delta, execution_date)


class StaggeredLoad(CyclicalLoad):
    """
    Model for loads that can be freely moved throughout a day by and optimisation algorithm.

    e.g.: dishwasher, washing machine , ...
    """

    def __init__(self, power_consumption: float, original_start_time,
                 cycle_duration: float, execution_date: date=None, time_delta: pd.DateOffset=None, due_time: time=None):

        super().__init__(power_consumption, original_start_time, cycle_duration, time_delta, execution_date)

        self._due_time = 86400 if due_time is None else due_time.hour + 60*due_time.minute + 3600*due_time.second
        self._original_start_time = original_start_time

    @property
    def due_time(self) -> float:
        return self._due_time

    @property
    def original_start_time(self):
        return self._original_start_time
