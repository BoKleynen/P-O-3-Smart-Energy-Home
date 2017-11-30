import pandas as pd
import numpy as np

from datetime import datetime, date, time, timedelta
from house.house import House


class Simulation:
    def __init__(self, house: House):
        self.house = house

    def simulate_optimise(self, start: pd.Timestamp, end: pd.Timestamp):

        if self.house.has_solar_panel():
            irradiance_df = pd.read_csv(filepath_or_buffer="../../../data/Irradiance.csv",
                                        header=0,
                                        index_col="Date/Time",
                                        dtype={"watts-per-meter-sq": float},
                                        parse_dates=["Date/Time"]
                                        )
        else:
            irradiance_df = None

        if self.house.has_windmill():
            wind_speed_df = pd.read_csv(filepath_or_buffer="../../../data/wind_speed.csv",
                                        header=0,
                                        index_col="Date/Time",
                                        dtype={"meters-per-second": float},
                                        parse_dates=["Date/Time"]
                                        )
        else:
            wind_speed_df = None

        self.house.timestamp = start
        total_cost = 0

        while self.house.timestamp < end:
            self.house.optimise(irradiance_df, wind_speed_df)
            total_cost += self.house.advance_time(pd.Timedelta("1 days"), irradiance_df, wind_speed_df)

    def simulate_original(self, start: pd.datetime, end: pd.Timestamp):
        if self.house.has_solar_panel():
            irradiance_df = pd.read_csv(filepath_or_buffer="../../../data/Irradiance.csv",
                                        header=0,
                                        index_col="Date/Time",
                                        dtype={"watts-per-meter-sq": float},
                                        parse_dates=["Date/Time"]
                                        )
        else:
            irradiance_df = None

        if self.house.has_windmill():
            wind_speed_df = pd.read_csv(filepath_or_buffer="../../../data/wind_speed.csv",
                                        header=0,
                                        index_col="Date/Time",
                                        dtype={"meters-per-second": float},
                                        parse_dates=["Date/Time"]
                                        )
        else:
            wind_speed_df = None

        self.house.timestamp = start
        total_cost = 0

        while self.house.timestamp < end:
            self.house.optimise(irradiance_df, wind_speed_df)
            total_cost += self.house.advance_time(pd.Timedelta("1 days"), irradiance_df, wind_speed_df)

