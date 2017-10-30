import pandas as pd
import numpy as np
from datetime import datetime, date, time


average_wind_speed_path = "/Users/bokleynen/Documents/2Bir/P&O3/Smart-Energy-Home/data/Average-Wind-Speed.csv"
average_wind_speed_ds = pd.read_csv(average_wind_speed_path,
                                    index_col="Date/Time",
                                    converters={"miles-per-hour": lambda x: 0.44704 * float(x) if x != "" else np.nan},
                                    skiprows=8,
                                    parse_dates=True,
                                    infer_datetime_format=True
                                    )

irradiance_path = "/Users/bokleynen/Documents/2Bir/P&O3/Smart-Energy-Home/data/Irradiance.csv"
irradiance_ds = pd.read_csv(irradiance_path,
                            index_col="Date/Time",
                            skiprows=8,
                            parse_dates=True,
                            infer_datetime_format=True
                            )
