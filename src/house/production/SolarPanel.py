import math
from math import sin, cos
from datetime import date, datetime, timedelta
import pandas as pd
import numpy as np
from util.Util import *
import matplotlib.pyplot as plt
from matplotlib import dates


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

    # def power(self, t: datetime):
    #     return self.house.irradiance_data.at(t)[1] * self.peak_power/(1000 * self.area) * self.cos_theta(t)

    def _power(self, t, irradiance):
        return irradiance * self.peak_power/(1000 * self.area) * max(self.cos_theta(t), 0)

    def cos_theta(self, t: datetime) -> float:
        delta = SolarPanel.delta((t.date() - date(t.year, 1, 1)).days + 1)
        phi = 0.88839
        beta = self.inclination
        a_zs = self.orientation
        omega = SolarPanel.omega(t)

        return sin(delta)*sin(phi)*cos(beta) + sin(delta)*cos(phi)*sin(beta)*cos(a_zs) \
            + cos(delta)*cos(phi)*cos(beta)*cos(omega) - cos(delta)*sin(phi)*sin(beta)*cos(a_zs)*cos(omega) \
            - cos(delta)*sin(beta)*sin(a_zs)*sin(omega)

    @staticmethod
    def delta(n):
        # return 23.45 * math.pi/180 * math.sin(2*math.pi * (284 + n)/36.25)
        return -math.radians(23.44)*cos(math.radians(360/365*(n+10)))

    @staticmethod
    def omega(t: datetime):
        return math.pi/43200 * (t.hour*3600 + t.minute*60 - 43200)


