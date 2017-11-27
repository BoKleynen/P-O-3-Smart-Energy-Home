from house.production.SolarPanel import SolarPanel
import math
import matplotlib.pyplot as plt
from matplotlib import dates
from datetime import date, datetime, timedelta
import pandas as pd
import time
import numpy as np

solar_panel = SolarPanel(285.0, 0.64, 0, 1.540539, 1)

irradiance_df = pd.read_csv(filepath_or_buffer="../../../../data/Irradiance.csv",
                            header=0,
                            index_col="Date/Time",
                            dtype={"watts-per-meter-sq": float},
                            parse_dates=["Date/Time"]
                            )
print(irradiance_df)

# irradiance_df.to_csv("Irradiance.csv")
# hour_angle = [solar_panel.hour_angle(t) for t in pd.date_range(start, end, freq="300S")]
# solar_declination = [solar_panel.solar_declination(n) for n in range(365)]
# solar_azimuth = [solar_panel.solar_azimuth(t) for t in pd.date_range(start, end, freq="300S")]

# f = np.vectorize(solar_panel.incident_angle)
#
# data = f(pd.date_range(start, end, freq="300S").values)
#
# # print(math.fsum(map(lambda p: p * 300, data))*(2.77778*math.pow(10, -7)))
#
# plt.plot(data)
# plt.show()




