import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates
from util import Util
from datetime import datetime, date, time, timedelta


average_wind_speed_df = pd.read_csv(filepath_or_buffer="../../data/Average-Wind-Speed.csv",
                                    header=0,
                                    index_col="Date/Time",
                                    converters={"miles-per-hour": lambda x: 0.44704 * float(x) if x != "" else np.nan},
                                    skiprows=8,
                                    parse_dates=True,
                                    infer_datetime_format=True
                                    )

data = [np.mean(average_wind_speed_df.at_time(t)) for t in Util.time_range()]

date_list = [datetime(2017, 1, 1, hour=t.hour, minute=t.minute) for t in Util.time_range()]

fig, ax = plt.subplots()
ax.plot(date_list, data)
fig.autofmt_xdate()
ax.xaxis.set_major_formatter(dates.DateFormatter("%H:%M"))
plt.show()
