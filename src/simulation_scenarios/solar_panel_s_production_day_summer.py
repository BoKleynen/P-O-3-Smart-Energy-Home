from power_generators import SolarPanel
import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from house import House

irradiance_df = pd.read_csv(filepath_or_buffer="../../data/Irradiance.csv",
                            header=0,
                            index_col="Date/Time",
                            dtype={"watts-per-meter-sq": float},
                            parse_dates=["Date/Time"]
                            )

solar_panel = SolarPanel(285.0, 0.64, 0, 0.87, 1.540539, 20)
house = House([], (solar_panel,))

start = pd.Timestamp("2016-06-17 00:00:00")
end = pd.Timestamp("2016-06-17 23:55:00")
house.timestamp = start
irradiance = irradiance_df.loc[pd.Timestamp(house.date):pd.Timestamp(house.date) + pd.DateOffset(hours=23, minutes=55)]["watts-per-meter-sq"].values

plt.plot(house.power_production(irradiance, None))
plt.ylabel("Power[W]")
plt.gcf().autofmt_xdate()

plt.show()
