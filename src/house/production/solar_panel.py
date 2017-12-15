import math
import pandas as pd

from math import cos
import pyximport
pyximport.install()
from util.solar_angles import incident_angle


class SolarPanel:
    def __init__(self, peak_power: float, tilt_angle: float, azimuth: float, latitude: float, area: float,
                 nb_solar_panel: int=1, price: float=0.0):
        if peak_power < 0:
            raise Exception("Peak power should be non negative.")
        if area < 0:
            raise Exception("Area should be non negative.")
        if not isinstance(nb_solar_panel, int):
            raise TypeError("The number of solar panels must be an integer number")
        if nb_solar_panel < 1:
            raise Exception("The number of solar panels must be greater than or equal to 1")

        self._tilt_angle = tilt_angle % (2*math.pi)
        self._azimuth = azimuth % (2*math.pi)
        self._peak_power = peak_power
        self._area = area
        self._latitude = latitude
        self._nb_solar_panel = nb_solar_panel
        self._price = price

    @property
    def tilt_angle(self):
        return self._tilt_angle

    @property
    def azimuth(self):
        return self._azimuth

    @property
    def peak_power(self):
        return self._peak_power

    @property
    def area(self):
        return self._area

    @property
    def house(self):
        return self.house

    @property
    def latitude(self):
        return self._latitude

    @property
    def price(self):
        return self._nb_solar_panel * self.price

    def power_production(self, t: pd.Timestamp, irradiance: float) -> float:
        return self._nb_solar_panel * irradiance * self.peak_power/(1000 * self.area) \
               * max(cos(incident_angle(t, self.azimuth, self.tilt_angle, self.latitude)), 0)
