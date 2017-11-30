from house.production.wind_mill import *
from house.production.solar_panel import *
from house.loads import *
from house.battery import *
from house.house import *


# initializing loads
fridge = ContinuousLoad(90)
freezer = ContinuousLoad(90)

heating = TimedLoad(2400, )
led_tv = TimedLoad(60, )
stove = TimedLoad(7000, )
