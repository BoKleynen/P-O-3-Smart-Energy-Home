import math


class Windmill:
    def __init__(self, radius):
        self.radius = radius

    @staticmethod
    def power_production(wind_speed, area):
        return 0.163 * area * wind_speed
    
    def get_produced_power(self, t: float) -> float:
        pass
        # return Windmill.power_production(wind_speed, math.pi * pow(self.radius, 2.0))
