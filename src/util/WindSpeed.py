import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, date, time, timedelta


average_wind_speed_df = pd.read_csv(filepath_or_buffer="../../data/Average-Wind-Speed.csv",
                                    header=0,
                                    index_col="Date/Time",
                                    converters={"miles-per-hour": lambda x: 0.44704 * float(x) if x != "" else np.nan},
                                    skiprows=8,
                                    parse_dates=True,
                                    infer_datetime_format=True
                                    )
