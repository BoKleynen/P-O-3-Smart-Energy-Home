from abc import ABCMeta


"""
Base class for modelling all the loads in a house
"""


class Load(metaclass=ABCMeta):
    """
    Power_consumption: power consumed per unit time in watts
    """
    def __init__(self, power_consumption):
        self.power_consumption = power_consumption

"""
Model for loads that have a relatively constant drain throughout the day
"""


class ContinuousLoad(Load):
    def __init__(self, power_consumption):
        super().__init__(power_consumption)
        
"""
Model for loads that can be freely moved throughout a day by and optimisation algorithm
based on the forecasted weather
"""


class StaggeredLoad(Load):
    """
    power_consumption:
    cycle_duration: time needed to perform task once in seconds
    """
    def __init__(self, power_consumption, cycle_duration):
        super().__init__(power_consumption)
        self.cycle_duration = cycle_duration


"""
Model for loads that have a relatively fixed start time and duration
"""


class TimedLoad(Load.Load):
    def __init__(self, power_consumption, start_time, duration):
        super().__init__(power_consumption)
        self.start_time = start_time
        self.duration = duration
    
    def get_start_time(self):
        return self.start_time
    
    def get_duration(self):
        return self.duration