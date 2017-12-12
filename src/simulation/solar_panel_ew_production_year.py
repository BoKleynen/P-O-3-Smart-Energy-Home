from house.production.solar_panel import SolarPanel
from house.house import House
from math import pi
import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

irradiance_df = pd.read_csv(filepath_or_buffer="../../data/Irradiance.csv",
                            header=0,
                            index_col="Date/Time",
                            dtype={"watts-per-meter-sq": float},
                            parse_dates=["Date/Time"]
                            )

solar_panel_east = SolarPanel(285.0, 37*pi/180, -pi/2, 0.87, 1.540539, 10)
solar_panel_west = SolarPanel(285.0, 37*pi/180, pi/2, 0.87, 1.540539, 10)
house = House([], solar_panel_tp=(solar_panel_east, solar_panel_west))

start = pd.Timestamp("2016-05-24 00:00:00")
end = pd.Timestamp("2017-04-21 23:55:00")
date = pd.date_range(start, end, freq="300S")
power = [house.power_production(t, irradiance_df) for t in pd.date_range(start, end, freq="300S")]

date = [t.to_pydatetime() for t in date]
plt.plot(date, power)
plt.xlabel("Date")
plt.ylabel("Power[W]")

plt.show()
