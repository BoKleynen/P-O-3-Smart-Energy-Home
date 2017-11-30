import scipy.optimize as opt
import numpy as np
import random
import math
import pandas as pd
from house.Loads import Load, StaggeredLoad, TimedLoad, ContinuousLoad
from house.production.SolarPanel import SolarPanel
from house.production.WindMill import Windmill
from house.Battery import Battery
from typing import Iterable, List, Tuple
from datetime import date, time


DAY_SECONDS = 86400


class House:
    """
    A class of houses with certain appliances that are modelled as loads and possibly a given number
    of solar panels and/or windmills.
    """

    def __init__(self, load_it: Iterable[Load], solar_panel: Tuple[SolarPanel]=(), nb_solar_panel: int=0,
                 windmill: Windmill=None, nb_windmill: int=0, battery: Battery=None, latitude: float=50,
                 timestamp=pd.Timestamp("2016-05-24 00:00")):
        """

        :param load_it: An iterable containing all loads in the house
        :param solar_panel: The type of solar panel installed, None if no solar panels are installed
        :param nb_solar_panel: The amount of solar panels, will be set to 0 if the house has no solar panel
        :param windmill: The type of windmill installed, None if no windmill is installed
        :param nb_windmill: The amount of windmills installed, will be set to 0 if no windmill is installed
        :param position: tuple (longitude, latitude)
        """
        self._continuous_load_list = [load for load in load_it if isinstance(load, ContinuousLoad)]
        self._staggered_load_list = [load for load in load_it if isinstance(load, StaggeredLoad)]
        self._timed_load_list = [load for load in load_it if isinstance(load, TimedLoad)]
        self._solar_panel = solar_panel
        self._nb_solar_panel = nb_solar_panel if self.solar_panel is not None else 0
        self._windmill = windmill
        self._nb_windmill = nb_windmill if self.windmill is not None else 0
        self._battery = battery
        self._is_large_installation = math.fsum(map(lambda sp: sp.nb_solar_panel * sp.peak_power, self.solar_panel)) \
            if self.has_solar_panel() else 0 \
            + self.nb_windmill * self.windmill.power(self.windmill.max_wind_speed) \
            if self.has_windmill() else 0 > 10.0
        self._timestamp = timestamp

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
    def solar_panel(self) -> Tuple[SolarPanel]:
        return self._solar_panel

    # @solar_panel.setter
    # def solar_panel(self, solar_panel: SolarPanel):
    #     solar_panel._house = self
    #     self.solar_panel = solar_panel

    @property
    def nb_solar_panel(self) -> int:
        return self._nb_solar_panel

    @property
    def windmill(self) -> Windmill:
        return self._windmill

    # @windmill.setter
    # def windmill(self, windmill: Windmill):
    #     windmill._house = self
    #     self._windmill = windmill

    @property
    def nb_windmill(self) -> int:
        return self._nb_windmill

    @nb_windmill.setter
    def nb_windmill(self, nb_windmill: int):
        if self.has_windmill():
            self._nb_windmill = nb_windmill

    @property
    def battery(self) -> Battery:
        return self._battery

    @battery.setter
    def battery(self, battery: Battery):
        if battery is not None:
            Battery.house = self
            self._battery = battery

    @property
    def is_large_installation(self) -> bool:
        return self._is_large_installation

    @property
    def date(self) -> date:
        return self._timestamp.date()

    def has_windmill(self) -> bool:
        """

        :return: True if and only if the house has a windmill associated with it
        """
        return self.windmill is not None

    def has_solar_panel(self) -> bool:
        """

        :return: True if and only if the house has a solar panel associated with it
        """
        return len(self.solar_panel) != 0

    def has_battery(self) -> bool:
        return self.battery is not None

    def continuous_load_power(self) -> float:
        return math.fsum(
            map(
                lambda load: load.power,
                self.continuous_load_list
            )
        )

    def staggered_load_power(self, t: pd.Timestamp, t_arr: np.ndarray) -> float:
        if len(t_arr) != len(self.staggered_load_list):
            raise Exception("iterable length mismatch")

        return math.fsum(
            map(
                lambda i: self.staggered_load_list[i].power_consumption(t - t_arr[i])
                if t_arr[i] <= t < t_arr[i] + self.staggered_load_list[i].cycle_duration
                else 0,
                range(len(t_arr))
            )
        )

    def timed_load_power(self, t: pd.Timestamp) -> float:
        return math.fsum(
            map(
                lambda load: load.power(t - load.start_time)
                if load.start_time <= t < load.start_time + load.cycle_duration
                else 0,
                self.timed_load_list
            )
        )

    def total_load_power(self, t: pd.Timestamp, t_arr: np.ndarray):
        return self.continuous_load_power() + self.timed_load_power(t) + self.staggered_load_power(t, t_arr)

    def produced_own_power(self, t: pd.Timestamp) -> float:
        return self.windmill.power(t) if self.has_windmill() else 0 \
            + math.fsum(map(lambda solar_panel: solar_panel.power(), self.solar_panel))

    def total_power_consumption(self, t, t_arr):
        return self.total_load_power(t, t_arr) - self.produced_own_power(t)

    def _cost(self, t_arr: np.ndarray, irradiance, wind_speed) -> float:
        if len(t_arr) != len(self.staggered_load_list):
            raise Exception("iterable length mismatch")

        init_battery_charge = self.battery.stored_energy

        t = [t for t in pd.date_range(self.date, self.date + pd.DateOffset(days=1), freq="300S")] \
            + [load.start_timestamp for load in self.timed_load_list if load.execution_date == self.date] \
            + [load.start_timestamp + pd.DateOffset(seconds=load.cycle_duration) for load in self.timed_load_list
               if load.execution_date == self.date]
        for i in range(len(t_arr)):
            load = self.staggered_load_list[i]
            if load.execution_date == self.date:
                load_start_time = load.execution_date + pd.DateOffset(seconds=t_arr[i])
                t += [load_start_time, load_start_time + pd.DateOffset(seconds=load.cycle_duration)]
        for load in self.timed_load_list:
            if load.execution_date == self.date:
                t += [load.start_time, load.start_time + pd.DateOffset(seconds=load.cycle_duration)]
        t.sort()

        cost = 0.0

        for i in range(len(t)):
            time_delta = (t[i + 1] - t[i]).total_seconds()
            total_power = self.total_power_consumption(t[i], t_arr)
            battery_power = self.battery.power(time_delta, total_power)
            self.battery.use_energy(battery_power*time_delta)
            used_energy = time_delta * (total_power + battery_power)
            cost += self.electricity_cost(t[i], used_energy)

        self.battery.stored_energy = init_battery_charge

        return cost

    def optimise(self, irradiance: pd.DataFrame=None, wind_speed: pd.DataFrame=None) -> List[float]:
        init_guesses = np.array([random.random() * DAY_SECONDS for i in range(len(self.staggered_load_list))])

        cons = ({'type': 'ineq', 'fun': lambda t: DAY_SECONDS - (t[i] + self.staggered_load_list[i].cycle_duration)}
                for i in range(len(self.staggered_load_list)))

        res = opt.minimize(self._cost, init_guesses, constraints=cons, args=(irradiance, wind_speed))

        return res

    def set_staggered_load_times(self, t_it) -> None:
        if len(t_it) != len(self.staggered_load_list):
            raise Exception("iterable length mismatch")

        for i in range(len(self.staggered_load_list)):
            load = self.staggered_load_list[i]
            seconds = t_it[i] % 60
            minutes = int((t_it[i] % 3600) / 60)
            hours = int(t_it[i] / 3600)
            load.set_start_time(time(hours, minutes, seconds))

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
