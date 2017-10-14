from house import House
from . import Environment


class Simulation:
    def __init__(self, house, environment):
        if isinstance(house, House.House):
            self.house = house
        
        if isinstance(environment, Environment.Environment):
            self.environment = environment
            
    def run_simulation(self, start, end):
        pass

    def get_available_own_power(self, time):
        wind_energy = 0
        solar_energy = 0
        
        if self.house.has_windmill():
            wind_energy = self.house.nb_windmill * self.house.windmill.get_produced_power(self.environment.wind_speed[time])
            
        if self.house.has_solar_panel():
            solar_energy = self.house.nb_solar_panel * self.house.solar_panel.get_produced_power()
            
        return wind_energy + solar_energy - self.house.get_total_continuous_load()
