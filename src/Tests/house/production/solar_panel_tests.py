import matplotlib.pyplot as plt
import pandas as pd

from house.production.solar_panel import SolarPanel
from time import time
from util.solar_angles import incident_angle

start_time = time()

solar_panel = SolarPanel(285.0, 0.64, 0, 0.87, 1.540539, 20)

irradiance_df = pd.read_csv(filepath_or_buffer="../../../../data/Irradiance.csv",
                            header=0,
                            index_col="Date/Time",
                            dtype={"watts-per-meter-sq": float},
                            parse_dates=["Date/Time"]
                            )

start = pd.Timestamp("2016-06-17 00:00:00")
end = pd.Timestamp("2016-06-17 23:55:00")
# end = pd.Timestamp("2016-07-24 23:55:00")
times = pd.date_range(start, end, freq="300S")

data = [solar_panel.power_production(t, irradiance_df.loc[t].values[0]) for t in pd.date_range(start, end, freq="300S")]

times = [t.to_pydatetime() for t in times]
plt.plot(times, data)
print(time() - start_time)
plt.show()

