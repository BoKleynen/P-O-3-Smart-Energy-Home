import math


class Windmill:
    def __init__(self, radius, min_wind_speed, max_wind_speed):
        self.radius = radius
        self.min_wind_speed = min_wind_speed
        self.max_wind_speed = max_wind_speed
        self._house = None

    @property
    def house(self):
        return self._house

    @staticmethod
    def _power_production(wind_speed: float, area: float) -> float:
        """

        :param wind_speed:
        :param area:
        :return:
        """
        return 0.6125 * area * math.pow(wind_speed, 3)

    def power(self, wind_speed):
        """

        :param wind_speed:
        :return:
        """
        if wind_speed < self.min_wind_speed:
            return 0

        elif wind_speed < self.max_wind_speed:
            return self._power_production(wind_speed, math.pi * math.pow(self.radius, 2))

        else:
            return self._power_production(self.max_wind_speed, math.pi * math.pow(self.radius, 2))
