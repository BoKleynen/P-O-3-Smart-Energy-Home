import math


class Windmill:
    def __init__(self, radius):
        self.radius = radius

    @staticmethod
    def __power_production(wind_speed: float, area: float) -> float:
        return 0.163 * area * wind_speed

    def power_production(self, t):
        return self.__power_production(5, math.pi * math.pow(self.radius, 2))
