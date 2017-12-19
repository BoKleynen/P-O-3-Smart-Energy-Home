import pandas as pd
import math
from house.cars import *

from house import House


class Simulation:
    def __init__(self, house: House):
        self.house = house
        self.irradiance_df = pd.read_csv(filepath_or_buffer="/Users/bokleynen/Documents/2Bir/P&O3/Smart-Energy-Home/data/Irradiance.csv",
                                         header=0,
                                         index_col="Date/Time",
                                         dtype={"watts-per-meter-sq": float},
                                         parse_dates=["Date/Time"]
                                         )

        self.wind_speed_df = pd.read_csv(filepath_or_buffer="/Users/bokleynen/Documents/2Bir/P&O3/Smart-Energy-Home/data/wind_speed.csv",
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

        irradiance = None
        wind_speed = None
        self.house.optimise(irradiance, wind_speed)
        total_cost += self.house.optimised_day_cost(irradiance, wind_speed)
        self.house.advance_day()

        # while self.house.timestamp < end:
        #     irradiance = None
        #     wind_speed = None
        #     self.house.optimise(irradiance, wind_speed)
        #     total_cost += self.house.optimised_day_cost(irradiance, wind_speed)
        #     self.house.advance_day()

        return total_cost

    def simulate_original(self, start: pd.Timestamp, end: pd.Timestamp, use_own_energy=True):
        self.setup(start)
        total_cost = 0

        irradiance = None
        wind_speed = None
        total_cost += self.house.original_day_cost(irradiance, wind_speed)
        self.house.advance_day()

        # if use_own_energy:
        #     while self.house.timestamp < end:
        #         irradiance = None
        #         wind_speed = None
        #         total_cost += self.house.original_day_cost(irradiance, wind_speed)
        #         self.house.advance_day()
        #
        # else:
        #     new_sim = Simulation(house=House(self.house.staggered_load_list + self.house.timed_load_list + self.house.continuous_load_list))
        #     return new_sim.simulate_original()

        return total_cost
