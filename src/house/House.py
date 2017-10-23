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
    of solar panels and windmills.
    
    load_it: an iterable containing all loads in the house
    solar_panel: the type of solar panel installed, None if no solar panels are installed
    nb_solar_panels: the amount of solar panels, will be set to 0 if the house has no solar panel
    windmill: the type of windmill installed, None if no windmill is installed
    nb_windmill: the amount of windmills installed, will be set to 0 if no windmill is installed
    """
    def __init__(self, load_it: Iterable[Load], solar_panel: SolarPanel=None, nb_solar_panel: int=0,
                 windmill: Windmill=None, nb_windmill: int=0):
        self.continuous_load_list: List[ContinuousLoad] = [load for load in load_it if isinstance(load, ContinuousLoad)]
        self.staggered_load_list: List[StaggeredLoad] = [load for load in load_it if isinstance(load, StaggeredLoad)]
        self.timed_load_list: List[TimedLoad] = [load for load in load_it if isinstance(load, TimedLoad)]
        self.solar_panel: SolarPanel = solar_panel
        self.nb_solar_panel: int = nb_solar_panel if self.solar_panel is not None else 0
        self.windmill: Windmill = windmill
        self.nb_windmill: int = nb_windmill if self.windmill is not None else 0
        self.is_optimised = False

    """
    :return: True if and only if the house has a windmill associated with it
    """
    def has_windmill(self) -> bool:
        return self.windmill is not None
    
    """
    :return: True if and only if the house has a solar panel associated with it
    """
    def has_solar_panel(self) -> bool:
        return self.solar_panel is not None
    
    """
    :return: The total amount of continuous power draw
    """
    def get_total_continuous_load(self) -> float:
        total_load = 0
        
        for load in self.continuous_load_list:
            total_load += load.power_consumption

        return total_load

    """
    :return the power consumed by all timed loads at a time t
    """
    def get_timed_load_power(self, t: float) -> float:
        return math.fsum(
            map(lambda load: load.power_consumption(t)
                if load.start_duration <= t < load.start_duration + load.duration else 0, self.timed_load_list))

    """
    :return: the total amount of power produced by the house at a given time
    """
    def get_produced_own_power(self, t: float) -> float:
        return self.windmill.get_produced_power(t) + self.solar_panel.get_produced_power(t)

    """
    Optimises the start times of the staggered loads in this house
    """
    def optimise(self):
        init_guesses = np.array([random.random() * DAY_SECONDS for i in range(len(self.staggered_load_list))])

        def cost(t: List[float]) -> float:
            _cost = 0.0

            for i in range(len(self.staggered_load_list)):
                _cost += integrate.quad(lambda _t: min(
                    (self.get_timed_load_power(_t) +
                     self.staggered_load_list[i].power_consumption(_t) -
                     self.get_produced_own_power(_t)) * price(_t), 0.0), t[i],
                                        t[i] + self.staggered_load_list[i].cycle_duration)

            return _cost

        cons = ({'type': 'ineq', 'fun': lambda t: DAY_SECONDS - (t[i] + self.staggered_load_list[i])}
                for i in range(len(self.staggered_load_list)))

        res = opt.minimize(cost, init_guesses, constraints=cons)

        for i in range(len(res.x)):
            self.staggered_load_list[i].set_start_time(res.x[i])


def price(t):
    return 20 if 28800 < t <= 72000 else 10


