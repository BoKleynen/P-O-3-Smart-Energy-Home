from production import SolarPanel
from production import WindMill


class House:
    def __init__(self, load_list, solar_panel=None, nb_solar_panel=0, windmill=None):
        if isinstance(load_list, list):
            self.load_list = load_list
            
        if isinstance(solar_panel, SolarPanel.SolarPanel):
            solar_panel.house = self
            self.solar_panel = solar_panel
            
        if isinstance(windmill, WindMill.Windmill):
            self.windmill = windmill
            
        self.nb_solar_panel = nb_solar_panel
