from house.production.SolarPanel import SolarPanel
import math
import matplotlib.pyplot as plt
from matplotlib import dates
from datetime import date, datetime, timedelta
import pandas as pd
import numpy as np

solar_panel = SolarPanel(285.0, math.radians(37), math.pi, 1.540539)

irradiance_df = pd.read_csv(filepath_or_buffer="../../../../data/Irradiance.csv",
                            header=0,
                            index_col="Date/Time",
                            dtype={"watts-per-meter-sq": float},
                            skiprows=8,
                            parse_dates=["Date/Time"]
                            )
# irradiance_df.interpolate(method='time', inplace=True)

start = pd.Timestamp("2016-05-24 00:00")
end = pd.Timestamp("2017-04-21 23:55")

data = [solar_panel.omega(t) for t in pd.date_range(start, end, freq="300S")]

plt.plot(data)
plt.show()
