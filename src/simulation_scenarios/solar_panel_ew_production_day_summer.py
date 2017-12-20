from power_generators import SolarPanel
from house import House
from math import pi
import pandas as pd
import matplotlib.pyplot as plt

irradiance_df = pd.read_csv(filepath_or_buffer="../../data/Irradiance.csv",
                            header=0,
                            index_col="Date/Time",
                            dtype={"watts-per-meter-sq": float},
                            parse_dates=["Date/Time"]
                            )

solar_panel_east = SolarPanel(285.0, 37*pi/180, -pi/2, 0.87, 1.540539, 10)
solar_panel_west = SolarPanel(285.0, 37*pi/180, pi/2, 0.87, 1.540539, 10)
house = House([], solar_panel_tp=(solar_panel_east, solar_panel_west))

start = pd.Timestamp("2016-06-17 00:00:00")
end = pd.Timestamp("2016-06-17 23:55:00")
date = pd.date_range(start, end, freq="300S")
irradiance = irradiance_df.loc[pd.Timestamp(start.date()):pd.Timestamp(start.date()) + pd.DateOffset(hours=23, minutes=55)]["watts-per-meter-sq"].values
power = house.power_production(irradiance, None)

# date = [t.to_pydatetime() for t in pd.date_range(start, end, freq="300S")]
plt.plot(power)
plt.xlabel("Date")
plt.ylabel("Power[W]")
plt.gcf().autofmt_xdate()

plt.show()