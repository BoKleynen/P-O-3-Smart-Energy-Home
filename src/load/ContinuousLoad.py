from . import Load


class ContinuousLoad(Load.Load):
    def __init__(self, power):
        super().__init__(power)