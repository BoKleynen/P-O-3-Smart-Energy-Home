import math


class SolarPanel:
    
    def __init__(self, peak_power: float, inclination: float, orientation: float, area: float):
        """

        :param peak_power: a function approximating the power_consumption output of the solar panel
        :param inclination: the angle between the plane of the solar panel and the xy plane in degree
        :param orientation: the rotation around z axis with respect to the North in degree
        """
        self.inclination: float = inclination
        self.orientation: float = orientation
        self.peak_power: float = peak_power
        self.area: float = area

    def power_consumption(self, t, irradiance, solar_inclination):
        math.cos(math.fabs(solar_inclination - self.inclination)) * self.peak_power/(1000*self.area) * irradiance

