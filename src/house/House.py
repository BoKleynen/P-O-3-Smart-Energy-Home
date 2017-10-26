import scipy.integrate as integrate
import scipy.optimize as opt
import numpy as np
import random
import math
from house.Loads import Load, StaggeredLoad, TimedLoad, ContinuousLoad
from house.production.SolarPanel import SolarPanel
from house.production.WindMill import Windmill
from typing import Iterable, List


DAY_SECONDS = 86400


class House:
    """
    A class of houses with certain appliances that are modelled as loads and possibly a given number
    of solar panels and/or windmills.
    """

    def __init__(self, load_it: Iterable[Load], solar_panel: SolarPanel=None, nb_solar_panel: int=0,
                 windmill: Windmill=None, nb_windmill: int=0):
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
        self.is_optimised = False

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

    def get_continuous_load_power(self) -> float:
        """

        :return: The total amount of continuous power draw
        """
        total_load = 0
        
        for load in self.continuous_load_list:
            total_load += load.power_consumption

        return total_load

    def get_staggered_load_power(self, t: float, t_arr: np.ndarray) -> float:
        """

        :param t:
        :param t_arr:
        :return: The power consumed by all the staggered loads at time t
        """
        if len(t_arr) != len(self.staggered_load_list):
            raise Exception("iterable length mismatch")

        return math.fsum(map(lambda i: self.staggered_load_list[i].power_consumption(t - t_arr[i])
            if t_arr[i] <= t <= t_arr[i] + self.staggered_load_list[i].cycle_duration else 0, range(len(t_arr))))

    def get_timed_load_power(self, t: float) -> float:
        """
        return: The power consumed by all timed loads at a time t
        """
        return math.fsum(map(lambda load: load.power_consumption(t - load.start_time)
                    if load.start_time <= t <= load.start_time + load.cycle_duration else 0, self.timed_load_list))

    def get_produced_own_power(self, t: float) -> float:
        """

        :param t:
        :return: The total amount of power produced by the house at a given time
        """
        pass
        # return self.windmill.get_produced_power(t) + self.solar_panel.get_produced_power(t)

    def get_available_own_power(self, t: float) -> float:
        """

        :param t:
        :return: The amount of self produced power available for staggered loads at the given time t
        """
        return max(self.get_produced_own_power(t) - self.get_timed_load_power(t), 0.0)

    # TODO: add support for some kind of database object, storing needed data like electricity price, wind speed, ...
    def optimise(self) -> List[float]:
        """
        Computes the optimal timings for the staggered loads to start their job.

        :return: A list containing the optimal start times for the staggered loads in this house
        """

        def staggered_cost(t_arr: np.ndarray) -> float:
            """

            :param t_arr:
            :return:
            """
            if len(t_arr) != len(self.staggered_load_list):
                raise Exception("iterable length mismatch")

            return integrate.quad(lambda t: max((self.get_staggered_load_power(t, t_arr) - self.get_available_own_power(t))
                                                * price(t), 0.0), 0.0, DAY_SECONDS)[0]

        init_guesses = np.array([random.random() * DAY_SECONDS for i in range(len(self.staggered_load_list))])

        cons = ({'type': 'ineq', 'fun': lambda t: DAY_SECONDS - (t[i] + self.staggered_load_list[i])}
                for i in range(len(self.staggered_load_list)))

        res = opt.minimize(staggered_cost, init_guesses, constraints=cons)

        return res.x

    def set_staggered_load_times(self, t_list) -> None:
        """

        :param t_list:
        :return:
        """
        if len(t_list) != len(self.staggered_load_list):
            raise Exception("iterable length mismatch")

        for i in range(len(self.staggered_load_list)):
            self.staggered_load_list[i].set_start_time(t_list[i])


def price(t):
    """
    temporary function

    :param t:
    :return:
    """
    return 20 if 28800 < t <= 72000 else 10


