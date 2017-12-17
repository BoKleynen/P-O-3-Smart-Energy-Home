cimport numpy as cnp

cdef class Windmill:
    cdef float _area, _min_wind_speed, _max_wind_speed, price
    cdef int _nb_windmill

    @staticmethod
    cdef float _power_production(float wind_speed, float area)
    cpdef cnp.ndarray[float, ndim=1] power_production(self, cnp.ndarray[float, ndim=1] wind_speed_arr)
    cpdef float peak_power(self)


cdef class SolarPanel:
    cdef float _tilt_angle, _azimuth, _peak_power, _area, _latitude, _price
    cdef int _nb_solar_panel

    cdef cnp.ndarray[float, ndim=1] incident_angle(self, int year, int month, int day)
    cpdef cnp.ndarray[float, ndim=1] power_production(self, cnp.ndarray[float, ndim=1] irradiance_arr, int year, int month, int day)

cdef int day_of_year(int year, int month, int day)
cdef float solar_declination(int day_of_year)
cdef float hour_angle(int second_of_the_day)
cdef float solar_altitude(float second_of_the_day, float latitude, float solar_declination, float hour_angle)
cdef float solar_azimuth(float latitude, float solar_declination, float hour_angle, float solar_altitude)
