from abc import ABCMeta
from typing import Callable


class Load(metaclass=ABCMeta):
    """
    Base class for modelling all the loads in a house

    power consumption should be expressed in kW (= 1000W)
    time in seconds and relative to 00:00 when expressing a time of the day
    """

    def __init__(self, power_consumption: Callable[[float], float]):
        """

        :param power_consumption:
        """
        self.power_consumption: Callable[[float], float] = power_consumption


class ContinuousLoad(Load):
    """
    Model for loads that have a relatively constant drain throughout the day.

    e.g.: freezer, fridge, ...
    """

    def __init__(self, power_consumption: Callable[[float], float]):
        super().__init__(power_consumption)


class StaggeredLoad(Load):
    """
    Model for loads that can be freely moved throughout a day by and optimisation algorithm.

    e.g.: charging battery, dishwasher, washing machine , ...
    """

    def __init__(self, power_consumption: Callable[[float], float], cycle_duration: float, due_time: float):
        """

        :param power_consumption: A function taking one argument (of time) that describes the power consumption of this load,
            assumed to be zero outside of [self.start_time, self.start_time + self.cycle_duration].
            The parameter of this function should always be expressed relative to the start time of this load.
            This is due to the mutable nature of self.start_time of an instance of StaggeredLoad.
        :param cycle_duration:
        :param due_time:
        """
        super().__init__(power_consumption)
        self.cycle_duration = cycle_duration
        self.start_time: float = None
        self.due_time: float = due_time

    def set_start_time(self, t: float) -> None:
        self.start_time = t


class TimedLoad(Load):
    """
    Model for loads that have a relatively fixed start time and duration

    e.g.: cooking, watching television, ...
    """

    def __init__(self, power_consumption: Callable[[float], float], start_time: float, cycle_duration):
        """

        :param power_consumption: A function taking one argument (of time) that describes the power consumption of this load,
            assumed to be zero outside of [self.start_time, self.start_time + self.cycle_duration].
            This is done automatically due to the immutable nature of self.start_time of an instance of TimedLoad
        :param start_time:
        :param cycle_duration:
        """
        super().__init__(lambda t: power_consumption(t-start_time) if start_time <= t <= start_time + cycle_duration else 0)
        self.start_time: float = start_time
        self.cycle_duration: float = cycle_duration
