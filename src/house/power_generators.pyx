cimport numpy as cnp
import numpy as np
from libc.math cimport sin, cos, asin, acos, pi, pow


cdef class Windmill:
    def __init__(self, float area, float min_wind_speed, float max_wind_speed, int nb_windmill=1, float price=0.0):
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
        self._price = price

    @property
    def price(self):
        return self._nb_windmill * self._price

    @staticmethod
    cdef float _power_production(float wind_speed, float area):
        return 0.6125 * area * pow(wind_speed, 3)

    cpdef cnp.ndarray[float, ndim=1] power_production(self, cnp.ndarray[float, ndim=1] wind_speed_arr):
        cdef int i
        cdef cnp.ndarray[float, ndim=1] result_arr = np.zeros(288)

        for i in range(288):
            if wind_speed_arr[i] < self._min_wind_speed:
                result_arr[i] = 0

            elif wind_speed_arr[i] < self._max_wind_speed:
                result_arr[i] = Windmill._power_production(wind_speed_arr[i], self._area)

            else:
                result_arr[i] = self.peak_power()

        return result_arr

    cpdef float peak_power(self):
        return Windmill._power_production(self._max_wind_speed, self._area)


cdef class SolarPanel:
    def __init__(self, float peak_power, float tilt_angle, float azimuth, float latitude, float area,
                 int nb_solar_panel=1, float price=0.0):

        if peak_power < 0:
            raise Exception("Peak power should be non negative.")
        if area < 0:
            raise Exception("Area should be non negative.")
        if not isinstance(nb_solar_panel, int):
            raise TypeError("The number of solar panels must be an integer number")
        if nb_solar_panel < 1:
            raise Exception("The number of solar panels must be greater than or equal to 1")

        self._tilt_angle = tilt_angle % (2*pi)
        self._azimuth = azimuth % (2*pi)
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

    cdef cnp.ndarray[float, ndim=1] incident_angle(self, int year, int month, int day):
        cdef float s_altitude
        cdef float h_angle
        cdef float s_declination = solar_declination(day_of_year(year, month, day))
        cdef cnp.ndarray res_arr = np.zeros([288], dtype=float)
        cdef int i

        for i in range(288):
            h_angle = hour_angle(300*i)
            s_altitude = solar_altitude(300*i, self._latitude, s_declination, h_angle)
            res_arr[i] = acos(
                cos(s_altitude) * cos(solar_azimuth(self._latitude, s_declination, h_angle, s_altitude) - self._plane_azimuth)
                * sin(self._plane_tilt_angle) + sin(s_altitude) * cos(self._plane_tilt_angle)
            )

        return res_arr

    cpdef cnp.ndarray[float, ndim=1] power_production(self, cnp.ndarray[float, ndim=1] irradiance_arr,
                                                      int year, int month, int day):
        cdef int i
        cdef cnp.ndarray[float, ndim=1] cos_incident_angle = self.incident_angle(year, month, day)

        for i in range(288):
            cos_incident_angle[i] = max(cos(cos_incident_angle[i]), 0)

        return self._nb_solar_panel * self._peak_power/(1000 * self._area) * irradiance_arr * cos_incident_angle


cdef int day_of_year(int year, int month, int day):
    cdef int days[13]
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        days[:] = [0, 0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
    else:
        days[:] = [0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]

    return days[month] + day

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
