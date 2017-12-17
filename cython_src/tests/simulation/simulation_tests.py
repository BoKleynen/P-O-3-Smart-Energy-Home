import pandas as pd
import numpy as np
from simulation.simulation import Simulation
from datetime import *
from loads import ContinuousLoad, TimedLoad, StaggeredLoad
from power_generators import SolarPanel, Windmill
from house import House


start_t = datetime.now()

# initializing loads
fridge = ContinuousLoad(90)
freezer = ContinuousLoad(90)

led_tv = TimedLoad(60, 0, 3600)
stove = TimedLoad(5250, 0, 7200)

dishwasher = StaggeredLoad(900, 0, 9000)
washing_machine1 = StaggeredLoad(1000, 0, 5400)
tumble_drier = StaggeredLoad(power_consumption=2600,
                             original_start_time=0,
                             cycle_duration=2700,
                             )

cont_load_arr = np.array([freezer, fridge])
timed_load_arr = np.array([led_tv, stove])
stag_load_arr = np.array([dishwasher, washing_machine1, tumble_drier])

solar_panel = SolarPanel(285.0, 0.64, 0, 0.87, 1.540539, 10)
windmill = Windmill(9.448223734, 2.5, 12.75190283)

solar_panel_arr = np.array([solar_panel])
windmill_arr = np.array([windmill])

house = House(cont_load_arr, timed_load_arr, stag_load_arr, solar_panel_arr, windmill_arr)

simulation = Simulation(house)

print(simulation.simulate_original(date(2016, 5, 24), date(2016, 5, 25)))
print(simulation.simulate_optimise(date(2016, 5, 24), date(2016, 5, 25)))
# print(dishwasher.start_time)
# print(datetime.now() - start_t)
