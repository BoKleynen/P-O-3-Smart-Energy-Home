class Battery:
    """
    a class modelling a batter that can be used to store locally produced energy
    """

    def __init__(self, voltage: float, capacity: float, charge: float=0):
        self.voltage: float = voltage
        self.capacity: float = capacity
        self.charge: float = charge
        
    def get_voltage(self) -> float:
        return self.voltage
    
    def get_capacity(self) -> float:
        return self.capacity

    def get_charge(self) -> float:
        return self.charge
