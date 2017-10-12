from . import Load


"""
Model for loads that can be freely moved throughout a day by and optimisation algorithm
based on the forecasted weather
"""


class StaggeredLoad(Load.Load):
    """
    power_consumption:
    cycle_duration: time needed to perform task once in seconds
    """
    def __init__(self, power_consumption, cycle_duration):
        super().__init__(power_consumption)
        self.cycle_duration = cycle_duration
