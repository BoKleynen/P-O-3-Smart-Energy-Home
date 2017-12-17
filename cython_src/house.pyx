import math
import pandas as pd
import numpy as np
cimport loads as cl
cimport numpy as cnp
cimport power_generators as cpg
from loads import ContinuousLoad, TimedLoad, StaggeredLoad
from power_generators import Windmill, SolarPanel
from datetime import date

cdef class House:
    cdef cl.ContinuousLoad[:] _continuous_load_arr
    cdef cl.TimedLoad[:] _timed_load_arr
    cdef cl.StaggeredLoad[:] _staggered_load_arr
    cdef cpg.SolarPanel[:] _solar_panel_arr
    cdef cpg.Windmill[:] _windmill_arr

    cdef char _is_large_installation
    cdef char _is_optimised

    cdef int _year, _month, _day, _day_of_week


    def __init__(self,
                 cnp.ndarray[object, ndim=1] continuous_load_arr=np.empty(0, dtype=object),
                 cnp.ndarray[object, ndim=1] timed_load_arr=np.empty(0, dtype=object),
                 cnp.ndarray[object, ndim=1] staggered_load_arr=np.empty(0, dtype=object),
                 cnp.ndarray[object, ndim=1] solar_panel_arr=np.empty(0, dtype=object),
                 cnp.ndarray[object, ndim=1] windmill_arr=np.empty(0, dtype=object),
                 timestamp=pd.Timestamp("2016-05-24 00:00")):

        self._continuous_load_arr = continuous_load_arr
        self._timed_load_arr = timed_load_arr
        self._staggered_load_arr = staggered_load_arr
        self._solar_panel_arr = solar_panel_arr
        self._windmill_arr = windmill_arr

        self._is_large_installation = 1 if math.fsum(map(lambda sp: sp.peak_power, self._solar_panel_arr)) \
            + math.fsum(map(lambda wm: wm.peak_power(), self._windmill_arr)) >= 10000 else 0

        self._is_optimised = 0
        self._year = timestamp.year
        self._month = timestamp.month
        self._day = timestamp.day
        self._day_of_week = timestamp.dayofweek


    # @property
    # def continuous_load_arr(self):
    #     return self._continuous_load_arr
    #
    # @property
    # def staggered_load_arr(self):
    #     return self._staggered_load_arr
    #
    # @property
    # def timed_load_arr(self):
    #     return self._timed_load_arr
    #
    # @property
    # def solar_panel_arr(self):
    #     return self._solar_panel_arr
    #
    # @property
    # def windmill_arr(self):
    #     return self._windmill_arr

    @property
    def is_large_installation(self):
        return self._is_large_installation == 1

    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    @property
    def day(self):
        return self._month

    @property
    def date(self):
        return date(self._year, self._month, self._day)

    @property
    def day_of_week(self):
        return self._day_of_week

    def has_windmill(self):
        return self._windmill_arr.shape[0] != 0

    def has_solar_panel(self):
        return self._solar_panel_arr.shape[0] != 0


    cdef cnp.ndarray[double, ndim=1] continuous_load_power(self):
        cdef int i
        cdef double cont_load_power = 0.0
        for i in range(self._continuous_load_arr.shape[0]):
            cont_load_power += self._continuous_load_arr[i]._power_consumption

        return np.array([cont_load_power for _ in range(288)])

    cdef cnp.ndarray[double, ndim=1] timed_load_power(self):
        cdef int i, j
        cdef cl.TimedLoad load
        cdef cnp.ndarray[double, ndim=1] timed_load_power_arr = np.zeros(288)
        for j in range(self._timed_load_arr.shape[0]):
            load = self._timed_load_arr[j]

            for i in range(load._start_time/300, (load._start_time+load._cycle_duration)/300):
                timed_load_power_arr[i] += self._timed_load_arr[i].power_consumption

        return timed_load_power_arr

    cdef cnp.ndarray[double, ndim=1] original_staggered_load_power(self):
        cdef int i, j
        cdef cl.StaggeredLoad load
        cdef cnp.ndarray[double, ndim=1] original_staggered_load_power_arr = np.zeros(288)


        for j in range(self._staggered_load_arr.shape[0]):
            load = self._staggered_load_arr[j]

            for i in range(load._original_start_time/300, (load._original_start_time+load._cycle_duration)/300):
                original_staggered_load_power_arr[i] += load._power_consumption

        return original_staggered_load_power_arr

    cdef cnp.ndarray[double, ndim=1] optimised_staggered_load_power(self):
        if self._is_optimised == 0:
            raise Exception("This method can only be called upon a house that has been optimised")

        cdef int i, j
        cdef cl.StaggeredLoad load
        cdef cnp.ndarray[double, ndim=1] optimised_load_power_arr = np.zeros(288)

        for j in range(self._staggered_load_arr.shape[0]):
            load = self._staggered_load_arr[j]

            for i in range(load._start_time/300, (load._start_time+load._cycle_duration)/300):
                optimised_load_power_arr[i] += load._power_consumption

        return optimised_load_power_arr

    cdef cnp.ndarray[double, ndim=1] total_original_load_power(self):
        return self.continuous_load_power() + self.timed_load_power() + self.original_staggered_load_power()

    cdef cnp.ndarray[double, ndim=1] total_optimised_load_power(self):
        if not self._is_optimised:
            raise Exception("This method can only be called on a house that has been optimised")
        return self.continuous_load_power() + self.timed_load_power() + self.optimised_staggered_load_power()

    cdef cnp.ndarray[double, ndim=1] solar_power_production(self, cnp.ndarray[double, ndim=1] irradiance):
        cdef cnp.ndarray[double, ndim=1] solar_power_arr = np.zeros(288)
        cdef int i
        cdef cpg.SolarPanel solar_panel

        for i in range(self._solar_panel_arr.shape[0]):
            solar_panel = self._solar_panel_arr[i]
            solar_power_arr += solar_panel.power_production(irradiance, self.date.year, self.date.month, self.date.day)

        return solar_power_arr

    cdef cnp.ndarray[double, ndim=1] wind_power_production(self, cnp.ndarray[double, ndim=1] wind_speed):
        cdef cnp.ndarray[double, ndim=1] wind_power_arr = np.zeros(288)
        cdef int i
        cdef cpg.Windmill windmill

        for i in range(self._windmill_arr.shape[0]):
            windmill = self._windmill_arr[i]
            wind_power_arr += windmill.power_production(wind_speed)

        return wind_power_arr

    cdef cnp.ndarray[double, ndim=1] power_production(self, cnp.ndarray[double, ndim=1] irradiance, cnp.ndarray[double, ndim=1] wind_speed):
        return self.solar_power_production(irradiance) + self.wind_power_production(wind_speed)

    cdef double _cost_function(self, cl.StaggeredLoad load, int load_start_time, cnp.ndarray[double, ndim=1] power_consumption_arr):

        cdef cnp.ndarray[double, ndim=1] load_power_arr = np.zeros(288)
        cdef int i

        for i in range(load_start_time/300, (load_start_time+load._cycle_duration)/300):
            load_power_arr[i] += load._power_consumption

        cdef cnp.ndarray[double, ndim=1] _power_consumption_arr = power_consumption_arr + load_power_arr

        cdef double cost = 0.0

        for i in range(288):
            cost += self.electricity_cost(i*300, 2.77778e-7 * 300 * _power_consumption_arr[i])

        return cost

    cdef void optimise(self, irradiance, wind_speed):
        cdef cnp.ndarray[object, ndim=1] sorted_load_arr = np.ndarray(sorted(self._staggered_load_arr, key=lambda load: load._power_consumption * load._cycle_duration, reverse=True))
        cdef cnp.ndarray[double, ndim=1] power_consumption_arr = self.continuous_load_power() + self.timed_load_power() \
                                                                - self.power_production(irradiance, wind_speed)

        cdef int n
        cdef int t_start
        cdef int min_t_start
        cdef double min_cost
        cdef double cost
        cdef cl.StaggeredLoad load
        cdef cnp.ndarray[double, ndim=1] load_power_consumption_arr

        for n in range(sorted_load_arr.shape[0]):
            min_t_start = 0
            min_cost = 1.0/0.0
            load = sorted_load_arr[n]

            for t_start in range(0, 86400 - load._cycle_duration, 300):
                cost = self._cost_function(load, t_start, power_consumption_arr)

                if cost < min_cost:
                    min_cost = cost
                    min_t_start = t_start

            load._start_time = min_t_start
            load_power_consumption_arr = np.zeros(288, np.float64)
            for t_start in range(load._start_time/300, (load._start_time+load._cycle_duration)/300):
                load_power_consumption_arr[t_start] = load._power_consumption

            power_consumption_arr += load_power_consumption_arr

        self._is_optimised = True

    cdef double electricity_cost(self, int t, double consumed_energy):
        """

        :param t:
        :param consumed_energy: energy in kWh
                                negative values means that energy was produced by self
        :return:

            peak:       8:00 - 20:00 on weekdays
            off-peak:   20:00 - 8:00 and weekends
        """
        if self.is_large_installation:
            if consumed_energy >= 0:
                return 0.24 * consumed_energy

            else:
                if t/3600 < 8 or t/3600 >= 20 or self._day_of_week >= 5:
                    return 0.036 * consumed_energy

                else:
                    return 0.052 * consumed_energy

        else:
            return 0.24 * consumed_energy

    cpdef void advance_date(self):
        """
        monday is defined as day 0
        """
        cdef int month_days[13]

        if (self._year % 4 == 0 and self._year % 100 != 0) or (self._year % 400 == 0):
            month_days[:] = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        else:
            month_days[:] = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        self._day = self._day + 1 if self._day + 1 <= month_days[self._month] else 1

        if self._day == 1:
            if self._month == 12:
                self._month = 1
                self._year += 1

            else:
                self._month += 1

        self._day_of_week = (self._day_of_week + 1) % 7

    cpdef double optimised_day_cost(self, irradiance_df, wind_speed_df):
        cdef cnp.ndarray[double, ndim=1] irradiance = irradiance_df.loc[pd.Timestamp(self.date):pd.Timestamp(self.date)+pd.DateOffset(hours=23, minutes=55)]["watts-per-meter-sq"].values
        cdef cnp.ndarray[double, ndim=1] wind_speed = wind_speed_df.loc[pd.Timestamp(self.date):pd.Timestamp(self.date)+pd.DateOffset(hours=23, minutes=55)]["meters-per-second"].values
        self.optimise( irradiance, wind_speed)
        cdef cnp.ndarray[double, ndim=1] power_consumption = self.total_optimised_load_power() \
                                                            - self.power_production(irradiance, wind_speed)
        cdef double cost = 0.0
        cdef int i

        for i in range(288):
            cost += self.electricity_cost(300*i,  2.77778e-7 * 300 * power_consumption[i])

        return cost

    cpdef double original_day_cost(self, irradiance_df, wind_speed_df):
        cdef cnp.ndarray[double, ndim=1] irradiance = irradiance_df.loc[pd.Timestamp(self.date):pd.Timestamp(self.date)+pd.DateOffset(hours=23, minutes=55)]["watts-per-meter-sq"].values
        cdef cnp.ndarray[double, ndim=1] wind_speed = wind_speed_df.loc[pd.Timestamp(self.date):pd.Timestamp(self.date)+pd.DateOffset(hours=23, minutes=55)]["meters-per-second"].values
        cdef cnp.ndarray[double, ndim=1] power_consumption = self.total_original_load_power() \
                                                            - self.power_production(irradiance, wind_speed)
        cdef double cost = 0.0
        cdef int i

        for i in range(288):
            cost += self.electricity_cost(300*i,  2.77778e-7 * 300 * power_consumption[i])

        return cost
