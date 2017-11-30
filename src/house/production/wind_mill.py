import math


class Windmill:
    def __init__(self, area, min_wind_speed, max_wind_speed):
        if area < 0:
            raise Exception("Radius should be non negative.")
        if min_wind_speed < 0:
            raise Exception("Minimal wind speed should be non negative")
        if max_wind_speed < min_wind_speed:
            raise Exception("Maximal wind speed should be greater than the minimal wind speed")

        self.area = area
        self.min_wind_speed = min_wind_speed
        self.max_wind_speed = max_wind_speed
        self._house = None

    @property
    def house(self):
        return self._house

    @staticmethod
    def _power_production(wind_speed: float, area: float) -> float:
        return 0.6125 * area * math.pow(wind_speed, 3)

    def power(self, wind_speed: float):
        """

        :param wind_speed:
        :return:
        """
        if wind_speed < self.min_wind_speed:
            return 0

        elif wind_speed < self.max_wind_speed:
            return self._power_production(wind_speed, self.area)

        else:
            return self._power_production(self.max_wind_speed, self.area)
