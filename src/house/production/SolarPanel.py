import math
from math import sin, cos
import pandas as pd


class SolarPanel:
    
    def __init__(self, peak_power: float, inclination: float, orientation: float, area: float):
        """

        :param peak_power: a function approximating the power_consumption output of the solar panel
        :param inclination: the angle between the plane of the solar panel and the xy plane in degree
        :param orientation: the rotation around z axis with respect to the North in degree
        """
        if peak_power < 0:
            raise Exception("Peak power should be non negative.")
        if area < 0:
            raise Exception("Area should be non negative.")

        self._inclination = inclination % 2*math.pi
        self._orientation = orientation % 2*math.pi
        self._peak_power = peak_power
        self._area = area
        self._house = None

    @property
    def inclination(self):
        return self._inclination

    @property
    def orientation(self):
        return self._orientation

    @property
    def peak_power(self):
        return self._peak_power

    @property
    def area(self):
        return self._area

    @property
    def house(self):
        return self.house

    # def power(self, t: pd.Timestamp):
    #     return self.house.irradiance_data.at(t)[1] * self.peak_power/(1000 * self.area) * self.cos_theta(t)

    def _power(self, t: pd.Timestamp, irradiance) -> float:
        return irradiance * self.peak_power/(1000 * self.area) * max(self.cos_theta(t), 0)

    def cos_theta(self, t: pd.Timestamp) -> float:
        delta = SolarPanel.delta(t.dayofyear)
        phi = 0.889536142
        beta = self.inclination
        a_zs = self.orientation
        omega = SolarPanel.omega(t)

        return sin(delta)*sin(phi)*cos(beta) + sin(delta)*cos(phi)*sin(beta)*cos(a_zs) \
            + cos(delta)*cos(phi)*cos(beta)*cos(omega) - cos(delta)*sin(phi)*sin(beta)*cos(a_zs)*cos(omega) \
            - cos(delta)*sin(beta)*sin(a_zs)*sin(omega)

    @staticmethod
    def delta(n):
        return -0.409105177*cos(0.017214206*(n+10))

    @staticmethod
    def omega(t: pd.Timestamp):
        return math.pi/43200 * (t.hour*3600 + t.minute*60 - 43200)


