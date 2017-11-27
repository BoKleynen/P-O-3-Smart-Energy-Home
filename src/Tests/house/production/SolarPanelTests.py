from house.production.SolarPanel import SolarPanel
import math
import matplotlib.pyplot as plt
from matplotlib import dates
from datetime import date, datetime, timedelta
import pandas as pd
import matplotlib
import numpy as np

solar_panel = SolarPanel(285.0, 0.64, 0, 1.540539)

irradiance_df = pd.read_csv(filepath_or_buffer="../../../../data/Irradiance.csv",
                            header=0,
                            index_col="Date/Time",
                            dtype={"watts-per-meter-sq": float},
                            skiprows=8,
                            parse_dates=["Date/Time"]
                            )
# irradiance_df.interpolate(method='time', inplace=True)

start = pd.Timestamp("2016-07-20 00:00")
end = pd.Timestamp("2016-07-20 23:55")

# hour_angle = [solar_panel.hour_angle(t) for t in pd.date_range(start, end, freq="300S")]
# solar_declination = [solar_panel.solar_declination(n) for n in range(365)]
# solar_azimuth = [solar_panel.solar_azimuth(t) for t in pd.date_range(start, end, freq="300S")]

data = [solar_panel.power(t, irradiance_df.loc[t]) for t in pd.date_range(start, end, freq="300S")]

plt.plot(data)
plt.show()
