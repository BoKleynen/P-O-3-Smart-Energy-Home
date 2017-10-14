class SolarPanel:
    """
    inclination: the angle between the plane of the solar panel and the xy plane in degree
    orientation: the rotation around z axis with respect to the North in degree
    power_production: a function approximating the power_consumption output of the solar panel
    """
    
    def __init__(self, power_production, inclination, orientation):
        self.inclination = inclination
        self.orientation = orientation
    
    def get_inclination(self):
        return self.inclination
    
    def get_orientation(self):
        return self.orientation
    
    def get_produced_power(self):
        pass
