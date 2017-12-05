import scipy.optimize as opt
import numpy as np
import random
import math
import pandas as pd
from house.loads import Load, StaggeredLoad, TimedLoad, ContinuousLoad
from house.production.solar_panel import SolarPanel
from house.production.wind_mill import Windmill
from house.battery import Battery
from typing import Iterable, List, Tuple
from datetime import date, time


DAY_SECONDS = 86400


class House:
    """
    A class of houses with certain appliances that are modelled as loads and possibly a given number
    of solar panels and/or windmills.
    """

    def __init__(self, load_it: Iterable[Load], solar_panel_tp: Tuple[SolarPanel] = (),
                 windmill_tp: Tuple[Windmill] = (), battery_tp: Tuple[Battery] = (),
                 timestamp=pd.Timestamp("2016-05-24 00:00")):

        self._continuous_load_list = [load for load in load_it if isinstance(load, ContinuousLoad)]
        self._staggered_load_list = [load for load in load_it if isinstance(load, StaggeredLoad)]
        self._timed_load_list = [load for load in load_it if isinstance(load, TimedLoad)]
        self._solar_panel_tp = solar_panel_tp
        self._windmill_tp = windmill_tp
        self._battery_tp = battery_tp
        self._total_battery_power = math.fsum(map(lambda battery: battery.max_power, battery_tp))
        self._total_battery_capacity = math.fsum(map(lambda battery: battery.capacity, battery_tp))
        self._is_large_installation = math.fsum(map(lambda sp: sp.peak_power, self.solar_panel_tp)) \
            + math.fsum(map(lambda wm: wm.peak_power, self.windmill_tp)) >= 10000
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

    def continuous_load_power(self) -> float:
        return math.fsum(
            map(
                lambda load: load.power_consumption,
                self.continuous_load_list
            )
        )

    def staggered_load_power(self, t: pd.Timestamp, t_arr: np.ndarray) -> float:
        if len(t_arr) != len(self.staggered_load_list):
            raise Exception("iterable length mismatch")

        return math.fsum(
            map(
                lambda i: self.staggered_load_list[i].power_consumption
                if t_arr[i] <= 3600*t.hour + 60*t.minute + t.second < t_arr[i] + self.staggered_load_list[i].cycle_duration
                else 0,
                range(len(t_arr))
            )
        )

    def timed_load_power(self, t: pd.Timestamp) -> float:
        return math.fsum(
            map(
                lambda load: load.power_consumption
                if load.start_time <= 3600*t.hour + 60*t.minute + t.second < load.start_time + load.cycle_duration
                else 0,
                self.timed_load_list
            )
        )

    def optimised_staggered_load_power(self, t: pd.Timestamp):
        if not self._is_optimised:
            raise Exception("This method can only be called on a house that has been optimised")

        return math.fsum(
            map(
                lambda load: load.power_consumption
                if load.start_time <= 3600*t.hour + 60*t.minute <= load.start_time + load.cycle_duration
                else 0,
                self.staggered_load_list
            )
        )

    def original_staggered_load_power(self, t: pd.Timestamp):
        return math.fsum(
            map(
                lambda load: load.power_consumption
                if load.original_start_time <= 3600*t.hour + 60*t.minute <= load.original_start_time + load.cycle_duration
                else 0,
                self.staggered_load_list
            )
        )

    def total_load_power(self, t: pd.Timestamp, t_arr: np.ndarray):
        return self.continuous_load_power() + self.timed_load_power(t) + self.staggered_load_power(t, t_arr)

    def total_optimised_load_power(self, t: pd.Timestamp) -> float:
        if not self._is_optimised:
            raise Exception("This method can only be called on a house that has been optimised")
        return self.continuous_load_power() + self.timed_load_power(t) + self.optimised_staggered_load_power(t)

    def total_original_load_power(self, t: pd.Timestamp):
        return self.continuous_load_power() + self.timed_load_power(t) + self.original_staggered_load_power(t)

    def _cost_function(self, t_arr: np.ndarray, irradiance_df: pd.DataFrame, wind_speed_df: pd.DataFrame) -> float:
        if len(t_arr) != len(self.staggered_load_list):
            raise Exception("iterable length mismatch")

        init_battery_charge_tp = [battery.stored_energy for battery in self.battery_tp]
        t = [t for t in pd.date_range(self.date, self.date + pd.DateOffset(days=1), freq="300S")]
        cost = 0.0

        for i in range(len(t)-1):
            time_delta = 300
            total_power = \
                self.total_load_power(t[i], t_arr) \
                - math.fsum(map(lambda sp: sp.power_production(t[i], irradiance_df.loc[t[i]].values[0]), self.solar_panel_tp)) \
                - math.fsum(map(lambda wm: wm.power_production(wind_speed_df.loc[t[i]].values[0]), self.windmill_tp))

            battery_power_list = [battery.power(time_delta, battery.capacity/self.total_battery_capacity*total_power)
                                  for battery in self.battery_tp]
            for j in range(len(self.battery_tp)):
                self.battery_tp[j] -= battery_power_list[j]
            cost += self.electricity_cost(t[i], 2.77778e-7*time_delta*(total_power - math.fsum(battery_power_list)))

        for i in range(len(init_battery_charge_tp)):
            self.battery_tp[i].stored_energy = init_battery_charge_tp[i]

        return cost

    def optimise(self, irradiance_df: pd.DataFrame = None, wind_speed_df: pd.DataFrame = None) -> List[float]:
        init_guesses = np.array([random.random() * DAY_SECONDS for i in range(len(self.staggered_load_list))])

        cons = ({'type': 'ineq', 'fun':
                lambda t: self.staggered_load_list[i].due_time - (t[i] + self.staggered_load_list[i].cycle_duration)}
                for i in range(len(self.staggered_load_list)))

        res = opt.minimize(self._cost_function, init_guesses, constraints=cons, args=(irradiance_df, wind_speed_df))
        self._is_optimised = True

        self.set_staggered_load_times(res.x)

        return res

    def set_staggered_load_times(self, t_it) -> None:
        if len(t_it) != len(self.staggered_load_list):
            raise Exception("iterable length mismatch")

        for i in range(len(self.staggered_load_list)):
            load = self.staggered_load_list[i]
            seconds = int(t_it[i] % 60)
            minutes = int((t_it[i] % 3600) // 60)
            hours = int(t_it[i] // 3600)
            load.start_time = time(hours, minutes, seconds)

    def electricity_cost(self, t: pd.Timestamp, consumed_energy: float) -> float:
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
                if t.hour < 8 or t.hour >= 20 or t.dayofweek >= 6:
                    return 0.036 * consumed_energy

                else:
                    return 0.052 * consumed_energy

        else:
            return 0.24 * consumed_energy

    def advance_time(self, irradiance_df: pd.DataFrame, wind_speed_df: pd.DataFrame) -> float:
        if not self._is_optimised:
            raise Exception
        t = [t for t in pd.date_range(self.date, self.date + pd.DateOffset(days=1), freq="300S")]

        cost = 0.0
        for i in range(len(t)-1):
            time_delta = (t[i + 1] - t[i]).total_seconds()
            total_power = self.total_optimised_load_power(t[i]) \
                - math.fsum(map(lambda sp: sp.power_production(t[i], irradiance_df.loc[t[i]].values[0]), self.solar_panel_tp)) \
                - math.fsum(map(lambda wm: wm.power_production(wind_speed_df.loc[t[i]].values[0]), self.windmill_tp))
            battery_power_list = [
                battery.power(time_delta, battery.capacity / self.total_battery_capacity * total_power)
                for battery in self.battery_tp]
            for j in range(len(self.battery_tp)):
                self.battery_tp[j] -= battery_power_list[j]
            cost += self.electricity_cost(t[i], 2.77778e-7*time_delta*(total_power + math.fsum(battery_power_list)))

        self.timestamp += pd.DateOffset()
        self._is_optimised = False

        return cost

    # def original_day_cost(self, irradiance_df: pd.DataFrame, wind_speed_df: pd.DataFrame):
    #     cost = math.fsum(
    #         map(
    #             lambda load: self.electricity_cost(load.start_time, load.power_consumption * load.cycle_duration),
    #             self.timed_load_list
    #         )
    #     ) + math.fsum(
    #         map(
    #             lambda load: self.electricity_cost(load.original_start_time, load.power_consumption * load.cycle_duration),
    #             self.staggered_load_list
    #         )
    #     )
    #
    #     cost += math.fsum(
    #         map(
    #             lambda t: self.electricity_cost(t, -self.power_production(t,
    #                                                                       irradiance_df.loc[t].values[0],
    #                                                                       wind_speed_df.loc[t].values[0])
    #                                             ),
    #             pd.date_range()
    #         )
    #     )
