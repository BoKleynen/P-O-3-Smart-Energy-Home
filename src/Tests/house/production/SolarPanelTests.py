from house.production.SolarPanel import SolarPanel
import math
import matplotlib.pyplot as plt
from matplotlib import dates
from datetime import date, datetime, timedelta
from util.Util import *
import pandas as pd
import numpy as np


solar_panel = SolarPanel(285.0, math.radians(37), math.pi, 1.540539)

irradiance_df = pd.read_csv(filepath_or_buffer="../../../../data/Irradiance.csv",
                            header=0,
                            index_col="Date/Time",
                            dtype={"watts-per-meter-sq": float},
                            skiprows=8,
                            parse_dates=True,
                            infer_datetime_format=True,
                            )

# print(irradiance_df.loc[datetime(2016, 5, 24, 0, 0, 0).strftime("%Y-%m-%d %H:%M:%S")].values[0][0])

start = datetime(2017, 1, 1, 0, 0)
end = datetime(2017, 1, 1, 23, 55)

data = [solar_panel._power(t, irradiance_df.loc[t.strftime("%Y-%m-%d %H:%M")].values[0][0]) for t in datetime_range(start, end, timedelta(seconds=300))]
# data = [irradiance_df.loc[t.strftime("%Y-%m-%d %H:%M")].values[0][0] for t in datetime_range(start, end, timedelta(seconds=300))]
# data = [solar_panel.cos_theta(t) for t in datetime_range(start, end, timedelta(seconds=300))]
# data = [solar_panel.delta(n) for n in range(1, 365)]
# data = [solar_panel.omega(t) for t in datetime_range(start, end, timedelta(seconds=300))]

date_list = [datetime(2017, 7, 20, hour=t.hour, minute=t.minute) for t in time_range()]
fig, ax = plt.subplots()
ax.plot(date_list, data)
fig.autofmt_xdate()
ax.xaxis.set_major_formatter(dates.DateFormatter("%H:%M"))

# plt.plot(data)
plt.show()
