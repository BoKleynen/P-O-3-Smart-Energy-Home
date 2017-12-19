import math
import pandas as pd
import numpy as np
from src.house.battery import Battery, CarBattery
from typing import Iterable, List, Tuple
from datetime import date, time
from power_generators import SolarPanel, Windmill
from loads import ContinuousLoad, TimedLoad, StaggeredLoad


class House:
    def __init__(self, load_it: Iterable, solar_panel_tp=(),
                 windmill_tp=(), battery_tp=(), car_battery: CarBattery=None,
                 timestamp=pd.Timestamp("2016-05-24 00:00")):

        self._continuous_load_list = [load for load in load_it if isinstance(load, ContinuousLoad)]
        self._staggered_load_list = [load for load in load_it if isinstance(load, StaggeredLoad)]
        self._timed_load_list = [load for load in load_it if isinstance(load, TimedLoad)]
        self._solar_panel_tp = solar_panel_tp
        self._windmill_tp = windmill_tp
        self._battery_tp = battery_tp
        self._total_battery_power = math.fsum(map(lambda battery: battery.max_power, battery_tp))
        self._total_battery_capacity = math.fsum(map(lambda battery: battery.capacity, battery_tp))
        self._electrical_car_battery = car_battery
        self._is_large_installation = math.fsum(map(lambda sp: sp.peak_power, self.solar_panel_tp)) \
            + math.fsum(map(lambda wm: wm.peak_power(), self.windmill_tp)) >= 10000
        self._timestamp = timestamp
        self._is_optimised = False

    @property
    def continuous_load_list(self) -> List[ContinuousLoad]:
        return self._continuous_load_list

    @property
    def staggered_load_list(self) -> List[StaggeredLoad]:
        return self._staggered_load_list

    @property
    def timed_load_list(self) -> List[TimedLoad]:
        return self._timed_load_list

    @property
    def solar_panel_tp(self) -> Tuple[SolarPanel]:
        return self._solar_panel_tp

    @property
    def windmill_tp(self) -> Tuple[Windmill]:
        return self._windmill_tp

    @property
    def battery_tp(self) -> Tuple[Battery]:
        return self._battery_tp

    @property
    def is_large_installation(self) -> bool:
        return self._is_large_installation

    @property
    def date(self) -> date:
        return self._timestamp.date()

    @property
    def timestamp(self) -> pd.Timestamp:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, t: pd.Timestamp):
        self._timestamp = t

    @property
    def total_battery_capacity(self) -> float:
        return self._total_battery_capacity

    def has_windmill(self) -> bool:
        return len(self.windmill_tp) != 0

    def has_solar_panel(self) -> bool:
        return len(self.solar_panel_tp) != 0

    def has_battery(self) -> bool:
        return len(self.battery_tp) != 0

    def has_electrical_car(self) -> bool:
        return self._electrical_car_battery is not None

    def continuous_load_power(self) -> np.ndarray:
        arr = np.zeros(288)

        for load in self.continuous_load_list:
            arr += load.day_power_consumption()

        return arr

    def timed_load_power(self) -> np.ndarray:
        arr = np.zeros(288)

        for load in self.timed_load_list:
            arr += load.day_power_consumption()

        return arr

    def original_staggered_load_power(self) -> np.ndarray:
        arr = np.zeros(288)

        for load in self.staggered_load_list:
            arr += load.original_day_power_consumption()

        return arr

    def optimised_staggered_load_power(self):
        if not self._is_optimised:
            raise Exception("This method can only be called upon a house that has been optimised")

        arr = np.zeros(288)

        for load in self.staggered_load_list:
            arr += load.day_power_consumption()

        return arr

    def solar_power_production(self, irradiance_arr) -> np.ndarray:
        arr = np.zeros(288)

        for solar_panel in self.solar_panel_tp:
            arr += solar_panel.day_power_production(irradiance_arr, self.timestamp.dayofyear)

        return arr

    def wind_power_production(self, wind_speed_arr) -> np.ndarray:
        arr = np.zeros(288)

        for windmill in self.windmill_tp:
            arr += windmill.power_production(wind_speed_arr)

        return arr

    def power_production(self, irradiance_arr, wind_speed_arr) -> np.ndarray:
        return self.solar_power_production(irradiance_arr) + self.wind_power_production(wind_speed_arr)

    def day_load_power(self, load, start_time):
        arr = np.zeros(288)

        for i in range(start_time//300, (start_time+load.cycle_duration)//300):
            arr[i] += load.power_consumption

        return arr

    def cost_function(self, load, start_time, power_arr) -> float:
        cost = 0.0
        arr = power_arr + self.day_load_power(load, start_time)

        for i in range(start_time//300, (start_time + load.cycle_duration) // 300):
            arr[i] += load.power_consumption

        for i in range(288):
            if self.is_large_installation:
                if arr[i] >= 0:
                    cost += 8.3333e-5 * 0.24 * arr[i]

                else:
                    if i < 96 or i >= 240 or self.timestamp.dayofweek >= 5:
                        cost += 8.3333e-5 * 0.036 * arr[i]

                    else:
                        cost += 8.3333e-5 * 0.052 * arr[i]

            else:
                cost += 8.3333e-5 * 0.24 * arr[i]

        return cost

    def optimise(self, irradiance, wind_speed_df):
        sorted_load_lst = sorted(self.staggered_load_list,
                                 key=lambda load: load.power_consumption * load.cycle_duration,
                                 reverse=True)
        power_consumption_arr = self.continuous_load_power() + self.timed_load_power() \
                                - self.power_production(irradiance, wind_speed_df)

        for load in sorted_load_lst:
            min_cost = math.inf
            min_t_start = 0

            for i in range((86400-load.cycle_duration)//300):
                cost = self.cost_function(load, i, power_consumption_arr)

                if cost < min_cost:
                    min_cost = cost
                    min_t_start = i

            load.start_time = 300 * min_t_start
            power_consumption_arr += load.day_power_consumption()

        self._is_optimised = True

    def large_installation_electricity_cost(self, t, power):
        """
            peak:       8:00 - 20:00 on weekdays
            off-peak:   20:00 - 8:00 on weekdays and weekends
        """
        if power >= 0:
            return 0.24 * power

        else:
            if t < 28800 or t >= 72000 or self.timestamp.dayofweek >= 6:
                return 0.036 * power
            else:
                return 0.052 * power

    def optimised_day_cost(self, irradiance, wind_speed):
        power_arr = self.optimised_staggered_load_power() + self.timed_load_power() + self.continuous_load_power() \
                    - self.power_production(irradiance, wind_speed)

        cost = 0.0
        if self._is_large_installation:
            for i in range(288):
                cost += self.large_installation_electricity_cost(300*i, power_arr[i])

        else:
            cost = power_arr.sum() * 5.3333e-5

        return cost

    def original_day_cost(self, irradiance, wind_speed):
        power_arr = self.original_staggered_load_power() + self.timed_load_power() + self.continuous_load_power() \
                    - self.power_production(irradiance, wind_speed)

        cost = 0.0
        if self._is_large_installation:
            for i in range(288):
                cost += self.large_installation_electricity_cost(300 * i, power_arr[i])

        else:
            cost = power_arr.sum() * 5.3333e-5

        return cost

    def advance_day(self):
        self._timestamp + pd.DateOffset()
