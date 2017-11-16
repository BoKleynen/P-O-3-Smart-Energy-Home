class Battery:
    """
    a class modelling a batter that can be used to store locally produced energy
    """

    def __init__(self, capacity: float, max_power: float, stored_energy: float=0.0):
        self.capacity: float = capacity
        self.max_power: float = max_power
        self.stored_energy: float = stored_energy

    def power(self, time_delta, needed_power):
        if needed_power > 0:
            if self.stored_energy - time_delta * min(needed_power, self.max_power) >= 0:
                self.stored_energy -= time_delta * min(needed_power, self.max_power)
                return min(needed_power, self.max_power)

            elif self.stored_energy - time_delta * min(self.stored_energy/time_delta, self.max_power):
                self.stored_energy -= time_delta * min(self.stored_energy/time_delta, self.max_power)
                return min(self.stored_energy/time_delta, self.max_power)

        else:
            return max(needed_power, -self.max_power)