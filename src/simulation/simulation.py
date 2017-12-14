import pandas as pd
import numpy as np

from datetime import datetime, date, time, timedelta
from house.house import House


class Simulation:
    def __init__(self, house: House):
        self.house = house
        self.irradiance_df = pd.read_csv(filepath_or_buffer="../../../data/Irradiance.csv",
                                         header=0,
                                         index_col="Date/Time",
                                         dtype={"watts-per-meter-sq": float},
                                         parse_dates=["Date/Time"]
                                         )

        self.wind_speed_df = pd.read_csv(filepath_or_buffer="../../../data/wind_speed.csv",
                                         header=0,
                                         index_col="Date/Time",
                                         dtype={"meters-per-second": float},
                                         parse_dates=["Date/Time"]
                                         )

    def setup(self, start: pd.Timestamp):
        for load in self.house.timed_load_list:
            load.execution_date = start.date()

        for load in self.house.staggered_load_list:
            load.execution_date = start.date()

        self.house.timestamp = start

    def simulate_optimise(self, start: pd.Timestamp, end: pd.Timestamp):
        self.setup(start)
        total_cost = 0

        while self.house.timestamp < end:
            self.house.optimise(self.irradiance_df, self.wind_speed_df)
            total_cost += self.house.advance_time(self.irradiance_df, self.wind_speed_df)

        return total_cost

    def simulate_original(self, start: pd.Timestamp, end: pd.Timestamp):
        self.setup(start)
        total_cost = 0

        while self.house.timestamp < end:
            total_cost += self.house.advance_time(self.irradiance_df, self.wind_speed_df)