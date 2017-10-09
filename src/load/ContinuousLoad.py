from . import Load


"""
Model for loads that have a relatively constant drain throughout the day
"""


class ContinuousLoad(Load.Load):
    def __init__(self, power):
        super().__init__(power)