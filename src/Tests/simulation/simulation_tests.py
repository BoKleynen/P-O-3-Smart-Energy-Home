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

led_tv = TimedLoad(60, time(hour=20, minute=30), 3600, pd.DateOffset())
stove = TimedLoad(5250, time(hour=11, minute=30), 7200, pd.DateOffset())

dishwasher = StaggeredLoad(900, time(hour=4), 9000, time_delta=pd.DateOffset())
washing_machine1 = StaggeredLoad(1000, time(hour=21), 5400, time_delta=pd.DateOffset())
tumble_drier = StaggeredLoad(power_consumption=2600,
                             original_start_time=None,
                             cycle_duration=2700,
                             )

loads = [dishwasher, washing_machine1, tumble_drier, led_tv, stove]
solar_panel = SolarPanel(285.0, 0.64, 0, 0.87, 1.540539, 5)
windmill = Windmill(1, 1, 10)

house = House(loads, (solar_panel,), (windmill,))

simulation = Simulation(house)

print(simulation.simulate_optimise(pd.Timestamp("2016-05-24 00:00:00"), pd.Timestamp("2016-05-24 23:55:00")))
for load in loads:
    print(load.start_time)

print()
print(datetime.now() - start_t)
