import pandas as pd
from libc.math cimport sin, cos, asin, acos, pi

cdef float solar_declination(day_of_year):
    return -0.409105177 * cos(0.017214206 * (day_of_year + 10))


cdef float hour_angle(t: pd.Timestamp):
    return pi / 43200 * (t.hour * 3600 + t.minute * 60 - 43200)


cdef float solar_altitude(t: pd.Timestamp, float latitude):
    cdef float h_angle = hour_angle(t)
    cdef float s_declination = solar_declination(t.dayofyear)

    return asin(
        cos(s_declination) * cos(latitude) * cos(h_angle)
        + sin(s_declination) * sin(latitude)
    )


cdef float solar_azimuth(t: pd.Timestamp, float latitude):
    return asin(
        cos(solar_declination(t.dayofyear)) * sin(hour_angle(t)) / cos(solar_altitude(t, latitude))
    )


cpdef float incident_angle(t: pd.Timestamp, float plane_azimuth, float plane_tilt_angle, float latitude):
    cdef float s_altitude = solar_altitude(t, latitude)

    return acos(
        cos(s_altitude) * cos(solar_azimuth(t, latitude) - plane_azimuth) * sin(plane_tilt_angle)
        + sin(s_altitude) * cos(plane_tilt_angle)
    )