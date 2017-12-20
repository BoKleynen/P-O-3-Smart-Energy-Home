from power_generators import SolarPanel
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from house import House
from math import pi


irradiance_df = pd.read_csv(filepath_or_buffer="../../data/Irradiance.csv",
                            header=0,
                            index_col="Date/Time",
                            dtype={"watts-per-meter-sq": float},
                            parse_dates=["Date/Time"]
                            )

solar_panel = SolarPanel(285.0, 0.64, 0, 0.87, 1.540539, 20)
solar_panel_east = SolarPanel(285.0, 37*pi/180, -pi/2, 0.87, 1.540539, 10)
solar_panel_west = SolarPanel(285.0, 37*pi/180, pi/2, 0.87, 1.540539, 10)

start = pd.Timestamp("2016-05-24 00:00:00")
end = pd.Timestamp("2017-04-21 23:55:00")
date = pd.date_range(start, end, freq="300S")

house_s = House([], (solar_panel,))
house_s.timestamp = start
irradiance = irradiance_df.loc[pd.Timestamp(house_s.date):pd.Timestamp(house_s.date) + pd.DateOffset(hours=23, minutes=55)][
    "watts-per-meter-sq"].values
power_s = house_s.power_production(irradiance, None)
house_s.advance_day()

while house_s.date < end.date():
    irradiance = irradiance_df.loc[pd.Timestamp(house_s.date):pd.Timestamp(house_s.date) + pd.DateOffset(hours=23, minutes=55)]["watts-per-meter-sq"].values
    power_s = np.concatenate((power_s, house_s.power_production(irradiance, None)))
    house_s.advance_day()


house_ew = House([], (solar_panel_east, solar_panel_west))
house_ew.timestamp = start
irradiance = irradiance_df.loc[pd.Timestamp(house_ew.date):pd.Timestamp(house_ew.date) + pd.DateOffset(hours=23, minutes=55)][
    "watts-per-meter-sq"].values
power_ew = house_ew.power_production(irradiance, None)
house_ew.advance_day()

while house_ew.date < end.date():
    irradiance = irradiance_df.loc[pd.Timestamp(house_ew.date):pd.Timestamp(house_ew.date) + pd.DateOffset(hours=23, minutes=55)]["watts-per-meter-sq"].values
    power_ew = np.concatenate((power_ew, house_ew.power_production(irradiance, None)))
    house_ew.advance_day()

plt.plot(power_s)
plt.plot(power_ew)
# plt.xlabel("Date")
plt.ylabel("Power[W]")

plt.show()
