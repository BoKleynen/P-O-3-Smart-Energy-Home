from . import Load


"""
Model for loads that can be freely moved throughout a day by and optimisation algorithm
based on the forecasted weather
"""


class StaggeredLoad(Load.Load):
    def __init__(self, power, cycle_duration):
        super().__init__(power)
        self.cycle_duration = cycle_duration

