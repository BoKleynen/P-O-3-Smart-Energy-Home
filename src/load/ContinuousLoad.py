from . import Load


"""
Model for loads that have a relatively constant drain throughout the day
"""


class ContinuousLoad(Load.Load):
    def __init__(self, power_consumption):
        super().__init__(power_consumption)