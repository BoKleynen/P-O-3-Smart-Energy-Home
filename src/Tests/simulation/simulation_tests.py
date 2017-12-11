from house.production.wind_mill import *
from house.production.solar_panel import *
from house.loads import *
from house.battery import *
from house.house import *
from house.battery import *
from simulation.simulation import *


# initializing loads
fridge = ContinuousLoad(90)
freezer = ContinuousLoad(90)

led_tv = TimedLoad(60, time(hour=20, minute=30), 3600, pd.DateOffset())
stove = TimedLoad(5250, time(hour=17, minute=30), 900, pd.DateOffset())

dishwasher = StaggeredLoad(900, time(hour=4), 9000, time_delta=pd.DateOffset())
washing_machine1 = StaggeredLoad(1000, time(hour=21), 5400, time_delta=pd.DateOffset())
tumble_drier = StaggeredLoad(power_consumption=2600,
                             original_start_time=None,
                             cycle_duration=2700,
                             constraints=[{'type': 'ineq',
                                           'fun': lambda _: tumble_drier.start_time - (washing_machine1.start_time + washing_machine1.cycle_duration)},
                                          {'type': 'ineq',
                                           'fun': lambda _: 86400 - (tumble_drier.start_time + tumble_drier.cycle_duration)}])

loads = [fridge, freezer, led_tv, stove, dishwasher, washing_machine1, tumble_drier]
solar_panel = SolarPanel(285.0, 0.64, 0, 0.87, 1.540539, 16)

house = House(loads, (solar_panel,))
simulation = Simulation(house)

print(simulation.simulate_optimise(pd.Timestamp("2016-05-24 00:00:00"), pd.Timestamp("2016-05-25 23:55:00")))
