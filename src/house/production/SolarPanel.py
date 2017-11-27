import math
from math import sin, cos, acos, asin
import pandas as pd


class SolarPanel:
    
    def __init__(self, peak_power: float, tilt_angle: float, azimuth: float, area: float):
        if peak_power < 0:
            raise Exception("Peak power should be non negative.")
        if area < 0:
            raise Exception("Area should be non negative.")

        self._tilt_angle = tilt_angle % (2*math.pi)
        self._azimuth = azimuth % (2*math.pi)
        self._peak_power = peak_power
        self._area = area
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

    def power(self, t: pd.Timestamp, irradiance) -> float:
        return irradiance * self.peak_power/(1000 * self.area) * max(cos(self.incident_angle(t)), 0)

    @staticmethod
    def solar_declination(n):
        return -0.409105177*cos(0.017214206*(n+10))

    @staticmethod
    def hour_angle(t: pd.Timestamp):
        return math.pi/43200 * (t.hour*3600 + t.minute*60 - 43200)

    def solar_altitude(self, t: pd.Timestamp):
        return asin(
            cos(self.solar_declination(t.dayofyear)) * cos(0.87) * cos(self.hour_angle(t))
            + sin(self.solar_declination(t.dayofyear)) * sin(0.87)
        )

    def solar_azimuth(self, t: pd.Timestamp):
        return asin(
            cos(self.solar_declination(t.dayofyear)) * sin(self.hour_angle(t)) / cos(self.solar_altitude(t))
        )

    def incident_angle(self, t: pd.Timestamp):
        return acos(
            cos(self.solar_altitude(t)) * cos(self.solar_azimuth(t) - self.azimuth) * sin(self.tilt_angle)
            + sin(self.solar_altitude(t)) * cos(self.tilt_angle)
        )
