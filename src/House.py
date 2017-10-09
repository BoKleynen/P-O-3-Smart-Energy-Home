class House:
    def __init__(self, roof):
        if isinstance(roof, Roof):
            self.roof = roof


class Roof:
    """
    area: the area of the roof
    inclination: the angle between the plane of the roof and the horizontal xy plane in degree
    orientation: the rotation around z axis with respect to the North in degree
    """
    
    def __init__(self, area, inclination, orientation):
        self.area = area
        self.inclination = inclination
        self.orientation = orientation

