from typing import Callable


class SolarPanel:
    
    def __init__(self, power_production: Callable[[float], float], inclination: float, orientation: float):
        """

        :param power_production: a function approximating the power_consumption output of the solar panel
        :param inclination: the angle between the plane of the solar panel and the xy plane in degree
        :param orientation: the rotation around z axis with respect to the North in degree
        """
        self.inclination: float = inclination
        self.orientation: float = orientation
        self.power_production: Callable[[float], float] = power_production
