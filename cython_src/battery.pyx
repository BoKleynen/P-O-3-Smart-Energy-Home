cimport numpy as cnp
import numpy as np
from libc.math cimport fmin, fmax, ceil


cdef class Battery:
    cdef double _capacity, _max_power, _stored_energy

    def __init__(self, double capacity, double max_power, double stored_energy):
        if capacity < 0:
            raise  Exception
        if stored_energy < 0:
            raise Exception
        if stored_energy > capacity:
            raise Exception

        self._capacity = capacity
        self._max_power = max_power
        self._stored_energy = stored_energy

    @property
    def capacity(self):
        return self._capacity

    @property
    def max_power(self):
        return self._max_power

    @property
    def stored_energy(self):
        return self._stored_energy

    @stored_energy.setter
    def stored_energy(self, stored_energy):
        if stored_energy < 0:
            raise Exception
        if stored_energy > self._capacity:
            raise Exception

        self._stored_energy = stored_energy

    cpdef double power(self, double req_power):
        cdef double power

        if req_power > 0:
            power = fmin(req_power, self._max_power)

            if self._stored_energy - 300 * power >= 0:
                return power

            else:
                return self._stored_energy/300

        else:
            power = fmax(req_power, -self._max_power)

            if self._stored_energy - 300 * power <= self._capacity:
                return power

            else:
                return -(self._capacity-self._stored_energy) / 300

    cpdef cnp.ndarray[double, ndim=1] day_power(self, cnp.ndarray[double, ndim=1] power_arr):
        cdef cnp.ndarray[double, ndim=1] arr = np.zeros(power_arr.shape[0])
        cdef int i
        cdef double power

        for i in range(power_arr.shape[0]):
            power = self.power(power_arr[i])
            arr[i] = power
            self._stored_energy = self._stored_energy - 300*power

        return arr


cdef class CarBattery(Battery):
    cdef double _daily_required_energy

    def __init__(self, double capacity, double max_power, double stored_energy, double daily_required_energy):
        super().__init__(capacity, max_power, stored_energy)

        if daily_required_energy < 0:
            raise Exception
        if daily_required_energy > capacity:
            raise Exception

        self._daily_required_energy = daily_required_energy


    @property
    def daily_required_energy(self):
        return self._daily_required_energy

    cpdef double power(self, double power):
        if power > 0:
            return 0

        else:
            if self._stored_energy - 300 * fmax(power, -self._max_power) <= self._capacity:
                return -fmax(power, -self._max_power)

            else:
                return (self._capacity-self._stored_energy) / 300

    cpdef cnp.ndarray[double, ndim=1] day_power(self, cnp.ndarray[double, ndim=1] power_arr):
        cdef cnp.ndarray[double, ndim=1] arr = np.zeros(power_arr.shape[0])
        cdef int i
        cdef double power
        cdef int nb_intervals = 0

        if self._stored_energy < self._daily_required_energy:
            nb_intervals = <int>ceil((self._daily_required_energy-self._stored_energy)/self._max_power/300)

        # 00:00 until 08:00
        for i in range(96-nb_intervals):
            power = self.power(power_arr[i])
            arr[i] = power
            self.stored_energy += 300*power

        # force charging the car
        for i in range(96-nb_intervals, 96):
            arr[i] = self._max_power
            self.stored_energy += 300 * self._max_power
            if self._stored_energy > self._daily_required_energy:
                break

        for i in range(96-nb_intervals+i, 96):
            power = self.power(power_arr[i])
            arr[i] = power
            self.stored_energy += 300*power

        # 08:00 until 18:00: car is not at home --> use 90% of the daily required energy
        self._stored_energy *= 0.1

        # 18:00 until 23:59
        for i in range(216, 288):
            power = self.power(power_arr[i])
            arr[i] = power
            self.stored_energy += 300*power

        return arr
