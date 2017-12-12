import matplotlib.pyplot as plt
import pandas as pd

from house.production.solar_panel import SolarPanel
from house.house import House
from math import pi
from time import time
from util.solar_angles import incident_angle

start_time = time()

solar_panel_east = SolarPanel(285.0, 37*pi/180, -pi/2, 0.87, 1.540539, 10)
solar_panel_west = SolarPanel(285.0, 37*pi/180, pi/2, 0.87, 1.540539, 10)

house = House([], solar_panel_tp=(solar_panel_east, solar_panel_west))

irradiance_df = pd.read_csv(filepath_or_buffer="data/Irradiance.csv",
                            header=0,
                            index_col="Date/Time",
                            dtype={"watts-per-meter-sq": float},
                            parse_dates=["Date/Time"]
                            )

start = pd.Timestamp("2016-06-17 00:00:00")
# end = pd.Timestamp("2017-04-21 23:55:00")
end = pd.Timestamp("2016-06-17 23:55:00")
times = pd.date_range(start, end, freq="300S")

data = [house.power_production(t, irradiance_df) for t in pd.date_range(start, end, freq="300S")]
# print(data)

plt.plot(data)
print(time() - start_time)
plt.show()
