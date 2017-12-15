import pandas as pd
import numpy as np
import math
from house.cars import *

from datetime import datetime, date, time, timedelta
from house.house import House


class Simulation:
    def __init__(self, house: House):
        self.house = house
        self.irradiance_df = pd.read_csv(filepath_or_buffer="C:\\Users\\Lander\\Documents\\KULeuven\\2e bachelor\\semester 1\\P&O 3\\P-O-3-Smart-Energy-Home\\data\\Irradiance.csv",
                                         header=0,
                                         index_col="Date/Time",
                                         dtype={"watts-per-meter-sq": float},
                                         parse_dates=["Date/Time"]
                                         )

        self.wind_speed_df = pd.read_csv(filepath_or_buffer="C:\\Users\\Lander\\Documents\\KULeuven\\2e bachelor\\semester 1\\P&O 3\\P-O-3-Smart-Energy-Home\\data\\wind_speed.csv",
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

    def simulate_original(self, start: pd.Timestamp, end: pd.Timestamp, use_own_energy=True):
        self.setup(start)
        total_cost = 0

        if use_own_energy:
            while self.house.timestamp < end:
                total_cost += self.house.original_day_cost(self.irradiance_df, self.wind_speed_df)
                self.house.timestamp += pd.DateOffset()

        else:
            new_sim = Simulation(house=House(self.house.staggered_load_list + self.house.timed_load_list + self.house.continuous_load_list))
            return new_sim.simulate_original()

        return total_cost

    def simulate_payback_period(self):
        year_cost_difference = self.simulate_optimise(pd.Timestamp("2016-05-24 00:00:00"), pd.Timestamp("2017-04-21 23:55:00")) \
                               - self.simulate_original(pd.Timestamp("2016-05-24 00:00:00"), pd.Timestamp("2017-04-21 23:55:00"), False)
        year_cost_difference *= 12/11

        purchase_difference = math.fsum(map(lambda wm: wm.price, self.house.windmill_tp)) \
                              + math.fsum(map(lambda sp: sp.price, self.house.solar_panel_tp)) \
                              + math.fsum(map(lambda bat: bat.price, self.house.battery_tp))

        if self.house.has_electrical_car():
            electrical_car = ElectricalCar(86100, 2016, 2016, None, None)
            original_car = PetrolCar(50000,) # TODO: add parameters
            purchase_difference += electrical_car.price() - electrical_car.subsidy() - original_car.price() - original_car.biv()

            year_cost_difference += original_car.costs() - electrical_car.costs()

        return purchase_difference / year_cost_difference
