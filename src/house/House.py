from solarPanel import SolarPanel


class House:
    def __init__(self, load_list, solar_panel, nb_solar_panel):
        if isinstance(load_list, list):
            self.load_list = load_list
            
        if isinstance(solar_panel, SolarPanel.SolarPanel):
            solar_panel.house = self
            self.solar_panel = solar_panel
            
        self.nb_solar_panel = nb_solar_panel
