from . import Roof


class House:
    def __init__(self, roof, appliance_list):
        if isinstance(roof, Roof.Roof):
            self.roof = roof
            
        if isinstance(appliance_list, list):
            self.appliance_list = appliance_list

