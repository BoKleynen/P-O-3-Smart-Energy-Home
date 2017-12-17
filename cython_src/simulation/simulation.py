import pandas as pd


class Simulation:
    def __init__(self, house):
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
        pass
        # for load in self.house.timed_load_arr:
        #     load.execution_date = start.date()
        #
        # for load in self.house.staggered_load_arr:
        #     load.execution_date = start.date()

        # self.house.timestamp = start

    def simulate_optimise(self, start, end):
        self.setup(start)
        total_cost = 0

        while self.house.date < end:
            self.house.optimise(self.irradiance_df, self.wind_speed_df)
            total_cost += self.house.optimised_day_cost(self.irradiance_df, self.wind_speed_df)
            self.house.advance_date()

        return total_cost

    def simulate_original(self, start, end, use_own_energy=True):
        self.setup(start)
        total_cost = 0

        if use_own_energy:
            while self.house.date < end:
                total_cost += self.house.original_day_cost(self.irradiance_df, self.wind_speed_df)
                self.house.advance_date()

        # else:
        #     new_sim = Simulation(house=House(self.house.staggered_load_list + self.house.timed_load_list + self.house.continuous_load_list))
        #     return new_sim.simulate_original()

        return total_cost
    #
    # def simulate_payback_period(self):
    #     year_cost_difference = self.simulate_optimise(pd.Timestamp("2016-05-24 00:00:00"), pd.Timestamp("2017-04-21 23:55:00")) \
    #                            - self.simulate_original(pd.Timestamp("2016-05-24 00:00:00"), pd.Timestamp("2017-04-21 23:55:00"), False)
    #     year_cost_difference *= 12/11
    #
    #     purchase_difference = math.fsum(map(lambda wm: wm.price, self.house.windmill_tp)) \
    #                           + math.fsum(map(lambda sp: sp.price, self.house.solar_panel_tp)) \
    #                           + math.fsum(map(lambda bat: bat.price, self.house.battery_tp))
    #
    #     if self.house.has_electrical_car():
    #         electrical_car = ElectricalCar(86100, 2016, 2016, None, None)
    #         original_car = PetrolCar(50000,) # TODO: add parameters
    #         purchase_difference += electrical_car.price() - electrical_car.subsidy() - original_car.price() - original_car.biv()
    #
    #         year_cost_difference += original_car.costs() - electrical_car.costs()
    #
    #     return purchase_difference / year_cost_difference
