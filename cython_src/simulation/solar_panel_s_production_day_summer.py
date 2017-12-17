from house.production.solar_panel import SolarPanel
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

solar_panel = SolarPanel(285.0, 0.64, 0, 0.87, 1.540539, 20)

start = pd.Timestamp("2016-06-17 00:00:00")
end = pd.Timestamp("2016-06-17 23:55:00")
date = pd.date_range(start, end, freq="300S")
power = [solar_panel.power_production(t, irradiance_df.loc[t].values[0]) for t in date]

date = [t.to_pydatetime() for t in date]
plt.plot(date, power)
plt.xlabel("Date")
plt.ylabel("Power[W]")
plt.gcf().autofmt_xdate()

plt.show()
