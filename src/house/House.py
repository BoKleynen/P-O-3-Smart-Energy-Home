import scipy.optimize as opt
import numpy as np
import random
import math
import pandas as pd
from house.Loads import Load, StaggeredLoad, TimedLoad, ContinuousLoad
from house.production.SolarPanel import SolarPanel
from house.production.WindMill import Windmill
from house.Battery import Battery
from typing import Iterable, List
from util.Util import *


DAY_SECONDS = 86400


class House:
    """
    A class of houses with certain appliances that are modelled as loads and possibly a given number
    of solar panels and/or windmills.
    """

    def __init__(self, load_it: Iterable[Load], solar_panel: SolarPanel=None, nb_solar_panel: int=0,
                 windmill: Windmill=None, nb_windmill: int=0, battery: Battery=None, position: tuple=None,
                 _date=date(2016, 1, 1), _time=time(0, 0, 0)):
        """

        :param load_it: An iterable containing all loads in the house
        :param solar_panel: The type of solar panel installed, None if no solar panels are installed
        :param nb_solar_panel: The amount of solar panels, will be set to 0 if the house has no solar panel
        :param windmill: The type of windmill installed, None if no windmill is installed
        :param nb_windmill: The amount of windmills installed, will be set to 0 if no windmill is installed
        :param position: tuple (longitude, latitude)
        """
        if solar_panel is not None and position is None:
            raise Exception("Position has to be known when solar panels are used")

        self._continuous_load_list = [load for load in load_it if isinstance(load, ContinuousLoad)]
        self._staggered_load_list = [load for load in load_it if isinstance(load, StaggeredLoad)]
        self._timed_load_list = [load for load in load_it if isinstance(load, TimedLoad)]
        self._solar_panel = solar_panel
        self._nb_solar_panel: int = nb_solar_panel if self.solar_panel is not None else 0
        self._windmill: Windmill = windmill
        self._nb_windmill: int = nb_windmill if self.windmill is not None else 0
        self._battery = battery
        self._is_large_installation = self.nb_solar_panel * self.solar_panel.peak_power \
            if self.has_solar_panel() else 0 \
            + self.nb_windmill * self.windmill.power(self.windmill.max_wind_speed) \
            if self.has_windmill() else 0 > 10.0
        self._position: tuple = position
        self._date = _date
        self._time = _time

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
    def solar_panel(self) -> SolarPanel:
        return self._solar_panel

    @solar_panel.setter
    def solar_panel(self, solar_panel: SolarPanel):
        solar_panel._house = self
        self.solar_panel = solar_panel

    @property
    def nb_solar_panel(self) -> int:
        return self._nb_solar_panel

    @property
    def windmill(self) -> Windmill:
        return self._windmill

    @windmill.setter
    def windmill(self, windmill: Windmill):
        windmill._house = self
        self._windmill = windmill

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
    def is_large_installation(self):
        return self._is_large_installation

    @property
    def position(self) -> tuple:
        return self._position

    @property
    def date(self) -> date:
        return self._date

    @property
    def time(self) -> time:
        return self.time

    @property
    def datetime(self) -> datetime:
        return datetime.combine(self.date, self.time)

    def has_windmill(self) -> bool:
        """

        :return: True if and only if the house has a windmill associated with it
        """
        return self.windmill is not None

    def has_solar_panel(self) -> bool:
        """

        :return: True if and only if the house has a solar panel associated with it
        """
        return self.solar_panel is not None

    def has_battery(self) -> bool:
        return self.battery is not None

    def continuous_load_power(self) -> float:
        """

        :return: The total amount of continuous power draw
        """
        return math.fsum(
            map(
                lambda load: load.power,
                self.continuous_load_list
            )
        )

    def staggered_load_power(self, t: datetime, t_arr: np.ndarray) -> float:
        """

        :param t:
        :param t_arr:
        :return: The power consumed by all the staggered loads at time t
        """
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

    def timed_load_power(self, t: datetime) -> float:
        """
        return: The power consumed by all timed loads at a time t
        """
        return math.fsum(
            map(
                lambda load: load.power(t - load.start_time)
                if load.start_time <= t < load.start_time + load.cycle_duration
                else 0,
                self.timed_load_list
            )
        )

    def total_load_power(self, t: datetime, t_arr: np.ndarray):
        return self.continuous_load_power() + self.timed_load_power(t) + self.staggered_load_power(t, t_arr)

    def produced_own_power(self, t: datetime) -> float:
        """

        :param t:
        :return: The total amount of power produced by the house at a given time
        """
        return self.windmill.power(t) if self.has_windmill() else 0 \
            + self.solar_panel.power(t) if self.has_solar_panel() else 0

    def total_power_consumption(self, t, t_arr):
        return self.total_load_power(t, t_arr) - self.produced_own_power(t)

    def _cost(self, t_arr: np.ndarray) -> float:
        """

        :param t_arr:
        :return:
        """
        if len(t_arr) != len(self.staggered_load_list):
            raise Exception("iterable length mismatch")

        init_battery_charge = self.battery.stored_energy

        start = datetime.combine(self.date, time(0, 0, 0))
        t = [t for t in datetime_range(start, start+timedelta(days=1), timedelta(seconds=300))] \
            + [load.start_datetime for load in self.timed_load_list if load.execution_date == self.date] \
            + [load.start_datetime + timedelta(seconds=load.cycle_duration) for load in self.timed_load_list
               if load.execution_date == self.date] \
            + [datetime.combine(self.staggered_load_list[i].execution_date, time(0, 0, 0)) + timedelta(seconds=t_arr[i])
               for i in range(len(t_arr)) if self.staggered_load_list[i].execution_date == self.date] \
            + [datetime.combine(self.staggered_load_list[i].execution_date, time(0, 0, 0))
               + timedelta(seconds=t_arr[i]+self.staggered_load_list[i].cycle_duration) for i in range(len(t_arr))
               if self.staggered_load_list[i].execution_date == self.date]

        t.sort()

        total_used_energy = 0.0
        cost = 0.0

        for i in range(len(t)):
            time_delta = (t[i + 1] - t[i]).total_seconds()
            total_power = self.total_power_consumption(t[i], t_arr)
            used_energy = time_delta * (total_power + self.battery.power(time_delta, total_power))
            total_used_energy += used_energy
            cost += self.electricity_cost(t[i], used_energy)

        return cost

    def optimise(self) -> List[float]:
        """
        Computes the optimal timings for the staggered loads to start their job.

        :return: A list containing the optimal start times for the staggered loads in this house
        """

        init_guesses = np.array([random.random() * DAY_SECONDS for i in range(len(self.staggered_load_list))])

        cons = ({'type': 'ineq', 'fun': lambda t: DAY_SECONDS - (t[i] + self.staggered_load_list[i])}
                for i in range(len(self.staggered_load_list)))

        res = opt.minimize(self._cost, init_guesses, constraints=cons)

        return res.x

    def set_staggered_load_times(self, t_it) -> None:
        """

        :param t_it: iterable containing times at which the staggered loads have to start their job, has to be ordered
        :return:
        """

        if len(t_it) != len(self.staggered_load_list):
            raise Exception("iterable length mismatch")

        for i in range(len(self.staggered_load_list)):
            self.staggered_load_list[i].start_time = t_it[i]

    def electricity_cost(self, t: datetime, consumed_energy) -> float:
        """

        :param t:
        :param consumed_energy: energy in kWh
        :return:

            peak:       8:00 - 20:00 on weekdays
            off-peak:   20:00 - 8:00 and weekends
        """
        if self.is_large_installation:
            if consumed_energy >= 0:
                return 0.24 * consumed_energy

            else:
                if t.time() < time(hour=8) or t.time() > time(hour=20) or t.isoweekday() >= 6:
                    return 0.036 * consumed_energy

                else:
                    return 0.052 * consumed_energy

        else:
            return 0.24 * consumed_energy
