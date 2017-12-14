class Battery:
    """
    a class modelling a battery that can be used to store locally produced energy
    """

    def __init__(self, capacity: float, max_power: float, stored_energy: float=0.0, price: float=0.0):
        if capacity < 0:
            raise Exception("Battery capacity has to be positive")
        if stored_energy < 0:
            raise Exception("Stored energy has to be positive")
        if stored_energy > capacity:
            raise Exception("Can't store more energy than the battery capacity")
        
        self._capacity = capacity
        self._max_power = max_power
        self._stored_energy = stored_energy
        self._price = price

    @property
    def capacity(self):
        return self._capacity

    @property
    def max_power(self):
        return self._max_power

    @property
    def stored_energy(self):
        return self._stored_energy

    @property
    def price(self):
        return self._price

    @stored_energy.setter
    def stored_energy(self, stored_energy: float):
        if stored_energy < 0:
            raise Exception("Stored energy has to be positive")
        if stored_energy > self.capacity:
            raise Exception("Can't store more energy than the battery capacity")
        self._stored_energy = 0.9*stored_energy

    def power(self, time_delta, power) -> float:
        if power > 0:
            if self.stored_energy - time_delta * min(power, self.max_power) >= 0:
                return min(power, self.max_power)

            elif self.stored_energy - time_delta * min(self.stored_energy/time_delta, self.max_power):
                return min(self.stored_energy/time_delta, self.max_power)

        else:
            if self.stored_energy - time_delta * max(power, -self.max_power) > self.capacity:
                return max((self.stored_energy-self.capacity)/time_delta, -self.max_power)

            else:
                return max(power, -self.max_power)


class CarBattery(Battery):
    def __init__(self, capacity: float, max_power: float, stored_energy: float=0.0, day_energy_req: float=0.0, price: float=0.0):
        super().__init__(capacity, max_power, stored_energy, price)
        if day_energy_req < 0:
            raise Exception("The daily energy requirement should be non negative")
        if day_energy_req > capacity:
            raise Exception("The daily energy requirement can't exceed battery capacity")
        self._day_energy_req = day_energy_req

    @property
    def daily_required_energy(self) -> float:
        return self._day_energy_req

    def power(self, time_delta, power):
        if power > 0:
            return 0

        else:
            if self.stored_energy - time_delta * max(power, -self.max_power) > self.capacity:
                return max((self.stored_energy - self.capacity) / time_delta, -self.max_power)

            else:
                return max(power, -self.max_power)

