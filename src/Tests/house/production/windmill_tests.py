import matplotlib.pyplot as plt
import pandas as pd

from house.production.WindMill import Windmill
from time import time

start_time = time()
windmill = Windmill(9.448223734, 2.5, 12.75190283)

wind_speed_df = pd.read_csv(filepath_or_buffer="/Users/bokleynen/Documents/2Bir/P&O3/Smart-Energy-Home/data/wind_speed.csv",
                            header=0,
                            index_col="Date/Time",
                            dtype={"meters-per-second": float},
                            parse_dates=["Date/Time"]
                            )

start = pd.Timestamp("2016-05-24 00:00:00")
# end = pd.Timestamp("2017-04-21 23:55:00")
end = pd.Timestamp("2016-05-24 23:55:00")
times = pd.date_range(start, end, freq="300S")

data = [windmill.power(wind_speed_df.loc[t].values[0]) for t in pd.date_range(start, end, freq="300S")]
# print(data)

plt.plot(data)
print(time() - start_time)
plt.show()
