
class Battery:
    def __init__(self, voltage, capacity, charge=0):
        self.voltage = voltage
        self.capacity = capacity
        self.charge = charge
        
    def get_voltage(self):
        return self.voltage
    
    def get_capacity(self):
        return self.capacity

    def get_charge(self):
        return self.charge
