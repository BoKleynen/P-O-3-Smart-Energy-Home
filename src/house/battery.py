class Battery:
    """
    a class modelling a battery that can be used to store locally produced energy
    """

    def __init__(self, capacity: float, max_power: float, stored_energy: float=0.0):
        if capacity < 0:
            raise Exception("Battery capacity has to be positive")
        if stored_energy < 0:
            raise Exception("Stored energy has to be positive")
        if stored_energy > capacity:
            raise Exception("Can't store more energy than the battery capacity")
        
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
    def stored_energy(self, stored_energy: float):
        if stored_energy < 0:
            raise Exception("Stored energy has to be positive")
        if stored_energy > self.capacity:
            raise Exception("Can't store more energy than the battery capacity")
        self._stored_energy = stored_energy

    def power(self, time_delta, needed_power):
        if needed_power > 0:
            if self.stored_energy - time_delta * min(needed_power, self.max_power) >= 0:
                return min(needed_power, self.max_power)

            elif self.stored_energy - time_delta * min(self.stored_energy/time_delta, self.max_power):
                return min(self.stored_energy/time_delta, self.max_power)

        else:
            return max(needed_power, -self.max_power)
        
    def use_energy(self, energy):
        self.stored_energy = self.stored_energy - energy
