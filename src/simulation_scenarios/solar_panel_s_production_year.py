from power_generators import SolarPanel
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from house import House

irradiance_df = pd.read_csv(filepath_or_buffer="../../data/Irradiance.csv",
                            header=0,
                            index_col="Date/Time",
                            dtype={"watts-per-meter-sq": float},
                            parse_dates=["Date/Time"]
                            )

solar_panel = SolarPanel(285.0, 0.64, 0, 0.87, 1.540539, 20)

start = pd.Timestamp("2016-05-24 00:00:00")
end = pd.Timestamp("2017-04-21 23:55:00")
date = pd.date_range(start, end, freq="300S")

house = House([], (solar_panel,))
house.timestamp = start
irradiance = irradiance_df.loc[pd.Timestamp(house.date):pd.Timestamp(house.date) + pd.DateOffset(hours=23, minutes=55)][
    "watts-per-meter-sq"].values
power = house.power_production(irradiance, None)
house.advance_day()

while house.date < end.date():
    irradiance = irradiance_df.loc[pd.Timestamp(house.date):pd.Timestamp(house.date) + pd.DateOffset(hours=23, minutes=55)]["watts-per-meter-sq"].values
    power = np.concatenate((power, house.power_production(irradiance, None)))
    house.advance_day()

date = [t.to_pydatetime() for t in date]
plt.plot(power)
plt.xlabel("Date")
plt.ylabel("Power[W]")

plt.show()
