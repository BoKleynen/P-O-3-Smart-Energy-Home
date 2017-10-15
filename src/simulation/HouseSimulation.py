import numpy as np
from scipy.optimize import minimize
from house import House
from . import Environment


"""
"""


class Simulation:
    def __init__(self, house, environment):
        if isinstance(house, House.House):
            self.house = house
        
        if isinstance(environment, Environment.Environment):
            self.environment = environment
            
    def run_simulation(self, start, end):
        pass
