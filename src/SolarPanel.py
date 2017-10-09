class SolarPanel:
    """
    inclination: the angle between the plane of the solar panel and the horizontal xy plane in degree
    orientation: the rotation around z axis with respect to the North in degree
    """
    
    def __init__(self, power, inclination, orientation):
        self.power = power
        self.inclination = inclination
        self.orientation = orientation
    
    def get_power(self):
        return self.power
    
    def get_inclination(self):
        return self.inclination
    
    def get_orientation(self):
        return self.orientation
