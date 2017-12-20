import pandas as pd
import matplotlib.pyplot as plt
from house import House
from simulation import Simulation
from datetime import datetime
from loads import ContinuousLoad, TimedLoad, StaggeredLoad
from power_generators import SolarPanel, Windmill
from battery import Battery, CarBattery

start_t = datetime.now()

fridge = ContinuousLoad(90)
freezer = ContinuousLoad(90)

led_tv = TimedLoad(60, 73800, 3600, 1)
stove = TimedLoad(5250, 63000, 900, 1)
led_lamps = TimedLoad(240, 72000, 14400, 1)
central_heating_1 = TimedLoad(2400, 23400, 9000, 1)
central_heating_2 = TimedLoad(2400, 64800, 9000, 1)
computer = TimedLoad(800, 75600, 7200, 1)
microwave = TimedLoad(1500, 64800, 600, 1)
hairdryer = TimedLoad(300, 27000, 600, 1)
hood = TimedLoad(150, 63000, 900, 1)
oven = TimedLoad(2500, 63000, 900, 1)

dishwasher = StaggeredLoad(900, 5200, 9600, 1)
washing_machine = StaggeredLoad(1000, 75600, 4800, 1)
tumble_dryer = StaggeredLoad(2600, 75600, 5400, 1)
boiler = StaggeredLoad(2000, 0, 16200, 1)
heat_pump_boiler = StaggeredLoad(700, 0, 16200, 1)

solar_panel = SolarPanel(285.0, 0.64, 0, 0.87, 1.540539, 20)
windmill = Windmill(9.448223734, 2.5, 12.75190283)
battery = Battery(4.86e+7, 5000, 0)

car_battery = CarBattery(2.7e+8, 16500, 0, 39420000)

loads = [fridge, freezer, led_tv, stove, dishwasher, washing_machine, tumble_dryer, led_lamps, central_heating_1, central_heating_2, computer, microwave, hairdryer, hood, boiler, heat_pump_boiler, oven]
house = House(loads,
              solar_panel_tp=(solar_panel,),
              windmill_tp=(windmill,),
              battery_tp=(battery,),
              car_battery=car_battery)
simulation = Simulation(house)

print("original: " + str(simulation.simulate_original(pd.Timestamp("2016-05-24").date(), pd.Timestamp("2016-06-24").date())))
print("optimised: " + str(simulation.simulate_optimise(pd.Timestamp("2016-05-24").date(), pd.Timestamp("2016-06-24").date())))
# print(simulation.simulate_payback_period(40000))
print(datetime.now() - start_t)
plt.show()
