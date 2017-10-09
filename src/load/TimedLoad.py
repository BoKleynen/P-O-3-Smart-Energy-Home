from . import Load


"""
Model for loads that have a relatively fixed start time and duration
"""


class TimedLoad(Load.Load):
    def __init__(self, power, start_time, duration):
        super().__init__(power)
        self.start_time = start_time
        self.duration = duration
