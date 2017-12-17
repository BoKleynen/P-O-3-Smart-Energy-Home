from datetime import date, time
import pandas as pd


cdef class Load:
    """
    Base class for modelling all the loads in a house

    power consumption should be expressed in kW (= 1000W)
    time in seconds and relative to 00:00 when expressing a time of the day
    """
    def __init__(self, float power_consumption):
        """

        :param power_consumption:
        """
        self._power_consumption = power_consumption

    @property
    def power_consumption(self):
        return self._power_consumption


cdef class ContinuousLoad(Load):
    """
    Model for loads that have a relatively constant drain throughout the day.

    e.g.: freezer, fridge, ...
    """

    def __init__(self, float power_consumption):
        super().__init__(power_consumption)


cdef class CyclicalLoad(Load):
    def __init__(self, float power_consumption, int start_time, int cycle_duration):

        super().__init__(power_consumption)

        # self._execution_date = execution_date
        self._start_time = start_time//300 * 300
        self._cycle_duration = cycle_duration//300 * 300
        # self._time_delta = time_delta if time_delta is not None else pd.DateOffset()

    # @property
    # def execution_date(self) -> date:
    #     return self._execution_date
    #
    # @execution_date.setter
    # def execution_date(self, execution_date: date):
    #     self._execution_date = execution_date

    @property
    def start_time(self) -> float:
        return self.start_time

    @start_time.setter
    def start_time(self, start_time: time):
        self._start_time = start_time

    # @property
    # def start_timestamp(self) -> pd.Timestamp:
    #     return pd.Timestamp.combine(self._execution_date, self._start_time)

    # @property
    # def time_delta(self) -> pd.DateOffset:
    #     return self._time_delta

    @property
    def cycle_duration(self) -> float:
        return self._cycle_duration


cdef class TimedLoad(CyclicalLoad):
    """
    Model for loads that have a relatively fixed start time and duration

    e.g.: cooking, watching television, ...
    """

    def __init__(self, float power_consumption, int start_time, int cycle_duration):

        super().__init__(power_consumption, start_time, cycle_duration)


cdef class StaggeredLoad(CyclicalLoad):
    """
    Model for loads that can be freely moved throughout a day by and optimisation algorithm.

    e.g.: dishwasher, washing machine , ...
    """
    def __init__(self, float power_consumption, int original_start_time, int cycle_duration):

        super().__init__(power_consumption, original_start_time, cycle_duration)

        self._original_start_time = original_start_time // 300 * 300

    @property
    def original_start_time(self):
        return self._original_start_time
