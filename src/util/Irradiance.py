import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates
from util import Util
from datetime import datetime, date, time, timedelta


irradiance_df = pd.read_csv(filepath_or_buffer="../../data/Irradiance.csv",
                            header=0,
                            index_col="Date/Time",
                            dtype={"watts-per-meter-sq": float},
                            skiprows=8,
                            parse_dates=True,
                            infer_datetime_format=True,
                            )

data = [np.mean(irradiance_df.at_time(t)) for t in Util.time_range()]
date_list = [datetime(2017, 1, 1, hour=t.hour, minute=t.minute) for t in Util.time_range()]

fig, ax = plt.subplots()
ax.plot(date_list, data)
fig.autofmt_xdate()
ax.xaxis.set_major_formatter(dates.DateFormatter("%H:%M"))
plt.show()
