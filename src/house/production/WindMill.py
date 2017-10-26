import math


class Windmill:
    def __init__(self, radius):
        self.radius = radius

    @staticmethod
    def power_production(wind_speed: float, area: float) -> float:
        return 0.163 * area * wind_speed
