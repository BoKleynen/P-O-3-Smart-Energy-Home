import math
from math import cos

import pandas as pd

from util.solar_angles import incident_angle


class SolarPanel:
    
    def __init__(self, peak_power: float, tilt_angle: float, azimuth: float, area: float, nb_solar_panel: int):
        if peak_power < 0:
            raise Exception("Peak power should be non negative.")
        if area < 0:
            raise Exception("Area should be non negative.")

        self._tilt_angle = tilt_angle % (2*math.pi)
        self._azimuth = azimuth % (2*math.pi)
        self._peak_power = peak_power
        self._area = area
        self._nb_solar_panel = nb_solar_panel
        self._house = None

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
    def nb_solar_panel(self):
        return self._nb_solar_panel

    def power(self, t: pd.Timestamp, irradiance) -> float:
        return irradiance * self.peak_power/(1000 * self.area) \
               * max(cos(incident_angle(t, self.azimuth, self.tilt_angle, 0.87)), 0)
