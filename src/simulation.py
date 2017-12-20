import pandas as pd
import math
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

    def setup(self, start):
        for load in self.house.timed_load_list:
            load.execution_date = start

        for load in self.house.staggered_load_list:
            load.execution_date = start

        self.house.timestamp = pd.Timestamp(start)

    def simulate_optimise(self, start, end):
        self.setup(start)
        total_cost = 0

        while self.house.date < end:
            date = self.house.date
            irradiance = \
            self.irradiance_df.loc[pd.Timestamp(date):pd.Timestamp(date) + pd.DateOffset(hours=23, minutes=55)][
                "watts-per-meter-sq"].values
            wind_speed = \
            self.wind_speed_df.loc[pd.Timestamp(date):pd.Timestamp(date) + pd.DateOffset(hours=23, minutes=55)][
                "meters-per-second"].values
            self.house.optimise(irradiance, wind_speed)
            total_cost += self.house.optimised_day_cost(irradiance, wind_speed)
            self.house.advance_day()

        return total_cost

    def simulate_original(self, start, end):
        self.setup(start)
        total_cost = 0

        while self.house.date < end:
            date = self.house.date
            irradiance = \
            self.irradiance_df.loc[pd.Timestamp(date):pd.Timestamp(date) + pd.DateOffset(hours=23, minutes=55)][
                "watts-per-meter-sq"].values
            wind_speed = \
            self.wind_speed_df.loc[pd.Timestamp(date):pd.Timestamp(date) + pd.DateOffset(hours=23, minutes=55)][
                "meters-per-second"].values
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
