from . import Load


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
