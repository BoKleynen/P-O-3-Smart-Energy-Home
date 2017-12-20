import pandas as pd
from house import House
from datetime import date


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
        self.init_battery_lst = [battery.stored_energy for battery in self.house.battery_tp]

        if self.house.has_electrical_car():
            self.init_car_battery_charge = self.house._electrical_car_battery.stored_energy

    def setup(self, start):
        for load in self.house.timed_load_list:
            load.execution_date = start

        for load in self.house.staggered_load_list:
            load.execution_date = start

        for i in range(len(self.init_battery_lst)):
            self.house.battery_tp[i].stored_energy = self.init_battery_lst[i]

        if self.house.has_electrical_car():
            self.house._electrical_car_battery.stored_energy = self.init_car_battery_charge

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

        return total_cost

    def simulate_payback_period(self, invest_cost):
        original_house = House([] + self.house.continuous_load_list + self.house.timed_load_list + self.house.staggered_load_list)
        original_simulation = Simulation(original_house)
        original_cost = 12/11*original_simulation.simulate_original(date(2016, 5, 24), date(2017, 4, 21))

        optimal_cost = 12/11*self.simulate_optimise(date(2016, 5, 24), date(2017, 4, 21))

        return invest_cost/(original_cost-optimal_cost)
