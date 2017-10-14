from house import Loads
from house.production import SolarPanel, WindMill


class House:
    def __init__(self, load_list, solar_panel=None, nb_solar_panel=0, windmill=None, nb_windmill=0):
        self.continuous_load_list = [load for load in load_list
                                     if isinstance(load, Loads.ContinuousLoad)]
        self.staggered_load_list = [load for load in load_list
                                    if isinstance(load, Loads.StaggeredLoad)]
        self.timed_load_list = [load for load in load_list if isinstance(load, Loads.TimedLoad)]
        
        if isinstance(solar_panel, SolarPanel.SolarPanel):
            self.solar_panel = solar_panel
            
        if isinstance(windmill, WindMill.Windmill):
            self.windmill = windmill
            
        self.nb_solar_panel = nb_solar_panel
        self.nb_windmill = nb_windmill

    def has_windmill(self):
        return self.windmill is not None
    
    def has_solar_panel(self):
        return self.solar_panel is not None
    
    def get_total_continuous_load(self):
        total_load = 0
        
        for load in self.continuous_load_list:
            total_load += load.power_consumption

        return total_load
