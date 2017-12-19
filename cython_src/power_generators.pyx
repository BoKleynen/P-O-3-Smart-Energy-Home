cimport numpy as cnp
import numpy as np
cimport numpy as cnp
from libc.math cimport sin, cos, asin, acos, pi, pow


cdef class Windmill:
    cdef float _area
    cdef float _min_wind_speed
    cdef float _max_wind_speed
    cdef int _nb_windmill

    def __init__(self, float area, float min_wind_speed, float max_wind_speed, int nb_windmill=1):
        if area < 0:
            raise Exception("Radius should be non negative.")
        if min_wind_speed < 0:
            raise Exception("Minimal wind speed should be non negative")
        if max_wind_speed < min_wind_speed:
            raise Exception("Maximal wind speed should be greater than the minimal wind speed")
        if not isinstance(nb_windmill, int):
            raise TypeError("The number of windmills must be an integer number")
        if nb_windmill < 1:
            raise Exception("The number of windmills must be greater or equal to 1")

        self._area = area
        self._min_wind_speed = min_wind_speed
        self._max_wind_speed = max_wind_speed
        self._nb_windmill = nb_windmill

    @staticmethod
    cdef float _power_production(float wind_speed, float area):
        return 0.6125 * area * pow(wind_speed, 3)

    cpdef float peak_power(self):
        return Windmill._power_production(self._max_wind_speed, self._area)

    cpdef float power_production(self, float wind_speed):
        if wind_speed < self._min_wind_speed:
                return 0

        elif wind_speed < self._max_wind_speed:
            return Windmill._power_production(wind_speed, self._area)

        else:
            return self.peak_power()

    cpdef cnp.ndarray[float, ndim=1] day_power_production(self, cnp.ndarray[float, ndim=1] wind_speed_arr):
        cdef int i
        cdef cnp.ndarray[float, ndim=1] arr = np.zeros(288)

        for i in range(288):
            arr[i] = self.power_production(wind_speed_arr[i])

        return arr


cdef class SolarPanel:
    cdef float _tilt_angle, _azimuth, _peak_power, _area, _latitude
    cdef int _nb_solar_panel

    def __init__(self, float peak_power, float tilt_angle, float azimuth, float latitude, float area, int nb_solar_panel=1):
        if peak_power < 0:
            raise Exception("Peak power should be non negative.")
        if area < 0:
            raise Exception("Area should be non negative.")
        if nb_solar_panel < 1:
            raise Exception("The number of solar panels must be greater than or equal to 1")

        self._tilt_angle = tilt_angle % (2*pi)
        self._azimuth = azimuth % (2*pi)
        self._peak_power = peak_power
        self._area = area
        self._latitude = latitude
        self._nb_solar_panel = nb_solar_panel

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

    cdef float incident_angle(self, int day_of_year, int t):
        cdef float h_angle = hour_angle(t)
        cdef float s_declination = solar_declination(day_of_year)
        cdef float s_altitude = solar_altitude(t, self._latitude, s_declination, h_angle)
        cdef cnp.ndarray res_arr = np.zeros([288], dtype=float)

        return acos(cos(s_altitude) * cos(solar_azimuth(self._latitude, s_declination, h_angle, s_altitude) - self._azimuth)
                * sin(self._tilt_angle) + sin(s_altitude) * cos(self._tilt_angle))

    cdef cnp.ndarray[float, ndim=1] day_incident_angle(self, int day_of_year):
        cdef float s_altitude
        cdef float h_angle
        cdef float s_declination = solar_declination(day_of_year)
        cdef cnp.ndarray res_arr = np.zeros([288], dtype=float)
        cdef int i

        for i in range(288):
            h_angle = hour_angle(300*i)
            s_altitude = solar_altitude(300*i, self._latitude, s_declination, h_angle)
            res_arr[i] = acos(
                cos(s_altitude) * cos(solar_azimuth(self._latitude, s_declination, h_angle, s_altitude) - self._azimuth)
                * sin(self._tilt_angle) + sin(s_altitude) * cos(self._tilt_angle)
            )

        return res_arr

    cpdef float power_production(self, irradiance, int day_of_year, int t):
        return self._nb_solar_panel * self._peak_power/(1000 * self._area) * irradiance * cos(self.incident_angle(day_of_year, t))

    cpdef cnp.ndarray[float, ndim=1] day_power_production(self, cnp.ndarray[float, ndim=1] irradiance_arr, int day_of_year):
        cdef int i
        cdef cnp.ndarray[float, ndim=1] cos_incident_angle = self.day_incident_angle(day_of_year)

        for i in range(288):
            cos_incident_angle[i] = max(cos(cos_incident_angle[i]), 0)

        return self._nb_solar_panel * self._peak_power/(1000 * self._area) * irradiance_arr * cos_incident_angle


cdef float solar_declination(int day_of_year):
    return -0.409105177 * cos(0.017214206 * (day_of_year + 10))


cdef float hour_angle(int second_of_the_day):
    return pi / 43200 * (second_of_the_day - 43200)


cdef float solar_altitude(float second_of_the_day, float latitude, float solar_declination, float hour_angle):
    return asin(
        cos(solar_declination) * cos(latitude) * cos(hour_angle)
        + sin(solar_declination) * sin(latitude)
    )


cdef float solar_azimuth(float latitude, float solar_declination, float hour_angle, float solar_altitude):
    return asin(
        cos(solar_declination) * sin(hour_angle) / cos(solar_altitude)
    )
