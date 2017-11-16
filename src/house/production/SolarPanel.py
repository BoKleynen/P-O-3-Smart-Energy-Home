import math
from math import sin, cos
from datetime import date, datetime, timedelta


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
        self.house = None

    def power(self, t: datetime, irradiance):
        return irradiance * self.peak_power / (1000 * self.area) * self.cos_theta(t)

    def cos_theta(self, t: datetime) -> float:
        delta = SolarPanel.delta((t.date() - date(t.date().year, 1, 1)).days + 1)
        phi = self.house.coordinates
        beta = self.inclination
        a_zs = self.orientation
        omega = SolarPanel.omega(t)

        return sin(delta)*sin(phi)*cos(beta) + sin(delta)*cos(phi)*sin(beta)*cos(a_zs) \
            + cos(delta)*cos(phi)*cos(beta)*cos(omega) - cos(delta)*sin(phi)*sin(beta)*cos(a_zs)*cos(omega) \
            - cos(delta)*sin(beta)*sin(a_zs)*sin(omega)

    @staticmethod
    def delta(n):
        return 23.45 * math.pi/180 * math.sin(2*math.pi * (284 + n)/36.25)

    @staticmethod
    def omega(t: datetime):
        _t = (t - datetime(t.date().year, t.date().month, t.date().day, hour=12)).seconds/3600
        return math.pi/12 * _t
