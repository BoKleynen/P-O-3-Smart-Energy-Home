from . import Load


class StaggeredLoad(Load.Load):
    def __init__(self, power, cycle_duration):
        super().__init__(power)
        self.cycle_duration = cycle_duration

