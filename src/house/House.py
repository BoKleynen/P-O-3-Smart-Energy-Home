import scipy.integrate as integrate
import scipy.optimize as opt
import numpy as np
import random
import math
from house.Loads import Load, StaggeredLoad, TimedLoad, ContinuousLoad
from house.production.SolarPanel import SolarPanel
from house.production.WindMill import Windmill
from house.Battery import Battery
from typing import Iterable, List
from datetime import datetime, date, time, timedelta


DAY_SECONDS = 86400


class House:
    """
    A class of houses with certain appliances that are modelled as loads and possibly a given number
    of solar panels and/or windmills.
    """

    def __init__(self, load_it: Iterable[Load], solar_panel: SolarPanel=None, nb_solar_panel: int=0,
                 windmill: Windmill=None, nb_windmill: int=0, battery: Battery=None):
        """

        :param load_it: An iterable containing all loads in the house
        :param solar_panel: The type of solar panel installed, None if no solar panels are installed
        :param nb_solar_panel: The amount of solar panels, will be set to 0 if the house has no solar panel
        :param windmill: The type of windmill installed, None if no windmill is installed
        :param nb_windmill: The amount of windmills installed, will be set to 0 if no windmill is installed
        """
        self.continuous_load_list: List[ContinuousLoad] = [load for load in load_it if isinstance(load, ContinuousLoad)]
        self.staggered_load_list: List[StaggeredLoad] = [load for load in load_it if isinstance(load, StaggeredLoad)]
        self.timed_load_list: List[TimedLoad] = [load for load in load_it if isinstance(load, TimedLoad)]
        self.solar_panel: SolarPanel = solar_panel
        self.nb_solar_panel: int = nb_solar_panel if self.solar_panel is not None else 0
        self.windmill: Windmill = windmill
        self.nb_windmill: int = nb_windmill if self.windmill is not None else 0
        self.battery = battery
        self.is_optimised = False
        battery.house = self
        self.is_large_installation = self.nb_solar_panel * self.solar_panel.peak_power if self.has_solar_panel() else 0\
            + self.nb_windmill * self.windmill.power(self.windmill.max_wind_speed) if self.has_windmill() else 0 > 10000.0
        self.coordinates = None

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

    def staggered_load_power(self, t: float, t_arr: np.ndarray) -> float:
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

    def timed_load_power(self, t: float) -> float:
        """
        return: The power consumed by all timed loads at a time t
        """
        return math.fsum(
            map(
                lambda load: load.power(t),
                self.timed_load_list
            )
        )

    def total_load_power(self, t: float, t_arr: np.ndarray):
        return self.continuous_load_power() + self.timed_load_power(t) + self.staggered_load_power(t, t_arr)

    def produced_own_power(self, t: float) -> float:
        """

        :param t:
        :return: The total amount of power produced by the house at a given time
        """
        return self.windmill.power(t) if self.has_windmill() else 0 \
            + self.solar_panel.power(t) if self.has_solar_panel() else 0

    def total_power_consumption(self, t, t_arr):
        return self.total_load_power(t, t_arr) - self.produced_own_power(t)

    def _staggered_cost(self, t_arr: np.ndarray) -> float:
        """

        :param t_arr:
        :return:
        """
        if len(t_arr) != len(self.staggered_load_list):
            raise Exception("iterable length mismatch")

        t = [t for t in range(0, DAY_SECONDS, 300)] \
            + [load.start_time for load in self.timed_load_list] \
            + [load.start_time + load.cycle_duration for load in self.timed_load_list] \
            + [t_arr[i] for i in range(len(t_arr))] \
            + [t_arr[i] + self.staggered_load_list[i].cycle_duration for i in range(len(t_arr))]

        t.sort()

        total_used_energy = 0.0
        cost = 0.0

        for i in range(len(t)):
            time_delta = t[i + 1] - t[i]
            total_power = self.total_power_consumption(t, t_arr)
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

        res = opt.minimize(self._staggered_cost, init_guesses, constraints=cons)

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
