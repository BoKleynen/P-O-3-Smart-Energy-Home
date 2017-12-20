import pandas as pd
from house import House
from simulation import Simulation
from datetime import datetime
from loads import ContinuousLoad, TimedLoad, StaggeredLoad
from power_generators import SolarPanel, Windmill
from battery import Battery

start_t = datetime.now()

# initializing loads
fridge = ContinuousLoad(90)
freezer = ContinuousLoad(90)

led_tv = TimedLoad(60, 0, 3600, 1)
stove = TimedLoad(5250, 0, 7200, 1)

dishwasher = StaggeredLoad(1000, 0, 9000, 1)
washing_machine1 = StaggeredLoad(1000, 0, 5400, 1)
tumble_drier = StaggeredLoad(2600, 0, 2700, 1)

battery = Battery(4.86e+7, 5000, 0)

loads = [led_tv, stove, dishwasher, washing_machine1, tumble_drier]
solar_panel = SolarPanel(285.0, 0.64, 0, 0.87, 1.540539, 20)
windmill = Windmill(9.448223734, 2.5, 12.75190283)

house = House(loads,
              solar_panel_tp=(solar_panel,),
              windmill_tp=(windmill,),
              battery_tp=(battery,)
              )

simulation = Simulation(house)

print("original: " + str(simulation.simulate_original(pd.Timestamp("2016-05-24").date(), pd.Timestamp("2016-05-25").date())))
print("optimised: " + str(simulation.simulate_optimise(pd.Timestamp("2016-05-24").date(), pd.Timestamp("2016-05-25").date())))
print(datetime.now() - start_t)
