import numpy as np
cimport numpy as cnp
from datetime import date


cdef class Load:
    cdef double _power_consumption

    def __init__(self, double power_consumption):
        self._power_consumption = power_consumption

    @property
    def power_consumption(self) -> double:
        return self._power_consumption


cdef class ContinuousLoad(Load):
    def __init__(self, double power_consumption):
        super().__init__(power_consumption)

    cpdef cnp.ndarray[double, ndim=1] day_power_consumption(self):
        cdef cnp.ndarray[double, ndim=1] arr = np.zeros(288)
        cdef int i

        for i in range(288):
            arr[i] = self._power_consumption

        return arr


cdef class CyclicalLoad(Load):
    cdef int _ex_year, _ex_month, _ex_day, _start_time, _cycle_duration, _ex_delta

    def __init__(self, double power_consumption, int start_time, int cycle_duration, int ex_delta):
        super().__init__(power_consumption)

        self._ex_year = 1
        self._ex_month = 1
        self._ex_day = 1

        self._start_time = start_time//300 * 300
        self._cycle_duration = cycle_duration//300 * 300
        self._ex_delta = ex_delta

    @property
    def execution_date(self) -> date:
        return date(self._ex_year, self._ex_month, self._ex_day)

    @execution_date.setter
    def execution_date(self, ex_date: date):
        self._ex_year = ex_date.year
        self._ex_month = ex_date.month
        self._ex_day = ex_date.day

    @property
    def start_time(self) -> int:
        return self._start_time

    @start_time.setter
    def start_time(self, start_time: int):
        self._start_time = start_time//300 * 300

    @property
    def cycle_duration(self) -> int:
        return self._cycle_duration

    @property
    def execution_delta(self) -> int:
        return self._ex_delta

    cpdef cnp.ndarray[double, ndim=1] day_power_consumption(self):
        cdef cnp.ndarray[double, ndim=1] arr = np.zeros(288)
        cdef int i

        for i in range(self._start_time/300, (self._start_time+self._cycle_duration)/300):
            arr[i] += self._power_consumption

        return arr


cdef class TimedLoad(CyclicalLoad):
    def __init__(self, double power_consumption, int start_time, int cycle_duration, int ex_delta):
        super().__init__(power_consumption, start_time, cycle_duration, ex_delta)


cdef class StaggeredLoad(CyclicalLoad):
    cdef int _original_start_time

    def __init__(self, double power_consumption, int original_start_time, int cycle_duration, int ex_delta):
        super().__init__(power_consumption, original_start_time, cycle_duration, ex_delta)

        self._original_start_time = original_start_time

    cpdef cnp.ndarray[double, ndim=1] original_day_power_consumption(self):
        cdef cnp.ndarray[double, ndim=1] arr = np.zeros(288)
        cdef int i

        for i in range(self._original_start_time/300, (self._original_start_time+self._cycle_duration)/300):
            arr[i] += self._power_consumption

        return arr

    @property
    def original_start_time(self):
        return self._original_start_time