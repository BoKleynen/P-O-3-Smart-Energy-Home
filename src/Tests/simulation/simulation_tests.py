from house.production.wind_mill import *
from house.production.solar_panel import *
from house.loads import *
from house.battery import *
from house.house import *
from house.battery import *
from simulation.simulation import *

start_t = datetime.now()

# initializing loads
fridge = ContinuousLoad(90)
freezer = ContinuousLoad(90)

led_tv = TimedLoad(60, time(hour=0), 3600, pd.DateOffset())
stove = TimedLoad(5250, time(hour=0), 7200, pd.DateOffset())

dishwasher = StaggeredLoad(900, time(hour=0), 9000, time_delta=pd.DateOffset())
washing_machine1 = StaggeredLoad(1000, time(hour=0), 5400, time_delta=pd.DateOffset())
tumble_drier = StaggeredLoad(power_consumption=2600,
                             original_start_time=time(hour=0),
                             cycle_duration=2700,
                             )

loads = [dishwasher, fridge, freezer, led_tv, washing_machine1, tumble_drier]
solar_panel = SolarPanel(285.0, 0.64, 0, 0.87, 1.540539, 1000)
windmill = Windmill(9.448223734, 2.5, 12.75190283)

house = House(loads, (solar_panel,))

simulation = Simulation(house)

print(simulation.simulate_original(pd.Timestamp("2016-05-24 00:00:00"), pd.Timestamp("2016-05-24 23:55:00")))
print(simulation.simulate_optimise(pd.Timestamp("2016-05-24 00:00:00"), pd.Timestamp("2016-05-24 23:55:00")))
print(datetime.now() - start_t)
