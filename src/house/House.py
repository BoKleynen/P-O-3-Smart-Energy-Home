from house import Loads
from house.production import SolarPanel, WindMill


class House:
    """
    A class of houses with certain appliances that are modelled as loads and possibly a given number
    of solar panels and windmills.
    
    load_it: an iterable containing all loads in the house
    solar_panel: the type of solar panel installed, None if no solar panels are installed
    nb_solar_panels: the amount of solar panels, will be set to 0 if the house has no solar panel
    windmill: the type of windmill installed, None if no windmill is installed
    nb_windmill: the amount of windmills installed, will be set to 0 if no windmill is installed
    """
    def __init__(self, load_it, solar_panel=None, nb_solar_panel=0, windmill=None, nb_windmill=0):
        self.continuous_load_list = [load for load in load_it
                                     if isinstance(load, Loads.ContinuousLoad)]
        self.staggered_load_list = [load for load in load_it
                                    if isinstance(load, Loads.StaggeredLoad)]
        self.timed_load_list = [load for load in load_it if isinstance(load, Loads.TimedLoad)]
        self.solar_panel = solar_panel if isinstance(solar_panel, SolarPanel.SolarPanel) else None
        self.windmill = windmill if isinstance(windmill, WindMill.Windmill) else None
        self.nb_solar_panel = nb_solar_panel if self.solar_panel is not None else 0
        self.nb_windmill = nb_windmill if self.windmill is not None else 0

    """
    :return: True if and only if the house has a windmill associated with it
    """
    def has_windmill(self):
        return self.windmill is not None
    
    """
    :return: True if and only if the house has a solar panel associated with it
    """
    def has_solar_panel(self):
        return self.solar_panel is not None
    
    """
    :return: The total amount of continuous power draw
    """
    def get_total_continuous_load(self):
        total_load = 0
        
        for load in self.continuous_load_list:
            total_load += load.power_consumption

        return total_load

    """
    :return: the total amount of power produced by the house at a given time
    """
    def get_available_own_power(self, time, wind_speed):
        wind_energy = 0
        solar_energy = 0
    
        if self.has_windmill():
            wind_energy = self.nb_windmill * self.windmill.get_produced_power(
                    wind_speed[time])
    
        if self.has_solar_panel():
            solar_energy = self.nb_solar_panel * self.solar_panel.get_produced_power()
    
        return wind_energy + solar_energy - self.get_total_continuous_load()

    def optimise(self):
        
        hourly_continuous_load = sum(load.power_consumption for load in self.continuous_load_list)
        
        for time in range(23):
            available_own_power = self.get_available_own_power(time, None)



