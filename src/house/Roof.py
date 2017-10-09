from .. import SolarPanel


class Roof:
    """
    solar_panel: the type of solar panel
    nb_solar_panel: the amount of solar panels on the roof
    """
    
    def __init__(self, solar_panel, nb_solar_panel):
        self.nb_solar_panel = nb_solar_panel
        if isinstance(solar_panel, SolarPanel.SolarPanel):
            self.solar_panel = solar_panel
    
    def get_solar_panel(self):
        return self.solar_panel
    
    def get_nb_solar_panel(self):
        return self.nb_solar_panel
