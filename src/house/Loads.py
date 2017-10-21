from abc import ABCMeta
from typing import Callable


"""
Base class for modelling all the loads in a house

power consumption should be expressed in kW (= 1000W)
time in seconds and relative to 00:00 when expressing a time of the day
"""


class Load(metaclass=ABCMeta):
    """
    Power_consumption: power consumed per unit time in watts
    """
    def __init__(self, power_consumption: Callable[[int]]):
        self.power_consumption = power_consumption


"""
Model for loads that have a relatively constant drain throughout the day.

e.g.: freezer, fridge, ...
"""


class ContinuousLoad(Load):
    def __init__(self, power_consumption: Callable[[int]]):
        super().__init__(power_consumption)
   
        
"""
Model for loads that can be freely moved throughout a day by and optimisation algorithm.

e.g.: charging battery, dishwasher, washing machine , ...
"""


class StaggeredLoad(Load):
    """
    power_consumption:
    cycle_duration: time needed to perform task once in seconds
    """
    def __init__(self, power_consumption: Callable[[int]], cycle_duration):
        super().__init__(power_consumption)
        self.cycle_duration = cycle_duration
        self.duration_constraint = lambda start, end: end - start + self.cycle_duration


"""
Model for loads that have a relatively fixed start time and duration

e.g.: cooking, watching television, ...
"""


class TimedLoad(Load):
    def __init__(self, power_consumption: Callable[[int]], start_time, duration):
        super().__init__(power_consumption)
        self.start_time = start_time
        self.duration = duration
