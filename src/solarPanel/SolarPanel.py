from house import House


class SolarPanel:
    """
    inclination: the angle between the plane of the solar panel and the xy plane in degree
    orientation: the rotation around z axis with respect to the North in degree
    power_production: a function approximating the power output of the solar panel
    """
    
    def __init__(self, power_production, inclination, orientation, house):
        self.power_production = power_production
        self.inclination = inclination
        self.orientation = orientation
        self.house = None
        
        if isinstance(house, House.House):
            self.house = house
    
    def get_power(self):
        pass
    
    def get_inclination(self):
        return self.inclination
    
    def get_orientation(self):
        return self.orientation
