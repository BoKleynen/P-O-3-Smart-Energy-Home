import math
import pandas as pd
from src.house.loads import Load, StaggeredLoad, TimedLoad, ContinuousLoad
from src.house.production.solar_panel import SolarPanel
from src.house.production.wind_mill import Windmill
from src.house.battery import Battery, CarBattery
from typing import Iterable, List, Tuple
from datetime import date, time


DAY_SECONDS = 86400


class House:
    def __init__(self, load_it: Iterable[Load], solar_panel_tp=(),
                 windmill_tp=(), battery_tp=(), car_battery: CarBattery=None,
                 timestamp=pd.Timestamp("2016-05-24 00:00"), electrical_car=None):

        self._continuous_load_list = [load for load in load_it if isinstance(load, ContinuousLoad)]
        self._staggered_load_list = [load for load in load_it if isinstance(load, StaggeredLoad)]
        self._timed_load_list = [load for load in load_it if isinstance(load, TimedLoad)]
        self._solar_panel_tp = solar_panel_tp
        self._windmill_tp = windmill_tp
        self._battery_tp = battery_tp
        self._total_battery_power = math.fsum(map(lambda battery: battery.max_power, battery_tp))
        self._total_battery_capacity = math.fsum(map(lambda battery: battery.capacity, battery_tp))
        self._electrical_car_battery = car_battery
        self._is_large_installation = math.fsum(map(lambda sp: sp.peak_power, self.solar_panel_tp)) \
            + math.fsum(map(lambda wm: wm.peak_power(), self.windmill_tp)) >= 10000
        self._timestamp = timestamp
        self._is_optimised = False
        self._constraints = []

    @property
    def continuous_load_list(self) -> List[ContinuousLoad]:
        return self._continuous_load_list

    @property
    def staggered_load_list(self) -> List[StaggeredLoad]:
        return self._staggered_load_list

    @property
    def timed_load_list(self) -> List[TimedLoad]:
        return self._timed_load_list

    @property
    def solar_panel_tp(self) -> Tuple[SolarPanel]:
        return self._solar_panel_tp

    @property
    def windmill_tp(self) -> Tuple[Windmill]:
        return self._windmill_tp

    @property
    def battery_tp(self) -> Tuple[Battery]:
        return self._battery_tp

    @property
    def is_large_installation(self) -> bool:
        return self._is_large_installation

    @property
    def date(self) -> date:
        return self._timestamp.date()

    @property
    def timestamp(self) -> pd.Timestamp:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, t: pd.Timestamp):
        self._timestamp = t

    @property
    def total_battery_capacity(self) -> float:
        return self._total_battery_capacity

    def has_windmill(self) -> bool:
        return len(self.windmill_tp) != 0

    def has_solar_panel(self) -> bool:
        return len(self.solar_panel_tp) != 0

    def has_battery(self) -> bool:
        return len(self.battery_tp) != 0

    def has_electrical_car(self) -> bool:
        return self._electrical_car_battery is not None

    def continuous_load_power(self) -> float:
        return math.fsum(
            map(
                lambda load: load.power_consumption,
                self.continuous_load_list
            )
        )

    def timed_load_power(self, t: pd.Timestamp) -> float:
        return math.fsum(
            map(
                lambda load: load.power_consumption
                if load.start_time <= 3600*t.hour + 60*t.minute + t.second < load.start_time + load.cycle_duration
                else 0,
                self.timed_load_list
            )
        )

    def original_staggered_load_power(self, t: pd.Timestamp):
        return math.fsum(
            map(
                lambda load: load.power_consumption
                if load.original_start_time <= 3600 * t.hour + 60 * t.minute < load.original_start_time + load.cycle_duration
                else 0,
                self.staggered_load_list
            )
        )

    def optimised_staggered_load_power(self, t: pd.Timestamp):
        if not self._is_optimised:
            raise Exception("This method can only be called upon a house that has been optimised")

        return math.fsum(
            map(
                lambda load: load.power_consumption
                if load.start_time <= 3600*t.hour + 60*t.minute < load.start_time + load.cycle_duration
                else 0,
                self.staggered_load_list
            )
        )

    def total_original_load_power(self, t: pd.Timestamp) -> float:
        return self.continuous_load_power() + self.timed_load_power(t) + self.original_staggered_load_power(t)

    def total_optimised_load_power(self, t: pd.Timestamp) -> float:
        if not self._is_optimised:
            raise Exception("This method can only be called on a house that has been optimised")
        return self.continuous_load_power() + self.timed_load_power(t) + self.optimised_staggered_load_power(t)

    def solar_power_production(self, t, irradiance):
        return math.fsum(map(lambda sp: sp.power_production(t, irradiance), self.solar_panel_tp))

    def wind_power_production(self, wind_speed):
        return math.fsum(map(lambda wm: wm.power_production(wind_speed), self.windmill_tp))

    def power_production(self, t: pd.Timestamp, irradiance_df: pd.DataFrame=None, wind_speed_df: pd.DataFrame=None):
        return math.fsum(map(lambda sp: sp.power_production(t, irradiance_df.loc[t].values[0]), self.solar_panel_tp)) \
            + math.fsum(map(lambda wm: wm.power_production(wind_speed_df.loc[t].values[0]), self.windmill_tp))

    def _interval_cost(self, t: pd.Timestamp, time_delta: float, power) -> float:
        battery_power_list = [
            battery.power(time_delta, battery.capacity / self.total_battery_capacity * power)
            for battery in self.battery_tp]
        for j in range(len(self.battery_tp)):
            self.battery_tp[j].stored_energy -= battery_power_list[j]
        return self.electricity_cost(t, 2.77778e-7 * time_delta * (power - math.fsum(battery_power_list)))

    def _interval_cost_charge_car(self, t: pd.Timestamp, time_delta: float, power) -> float:

        car_battery_power = self._electrical_car_battery.power(time_delta, power)
        self._electrical_car_battery.stored_energy -= car_battery_power
        power -= car_battery_power
        battery_power_list = [
            battery.power(time_delta, battery.capacity / self.total_battery_capacity * power)
            for battery in self.battery_tp]
        for j in range(len(self.battery_tp)):
            self.battery_tp[j].stored_energy -= battery_power_list[j]
        return self.electricity_cost(t, 2.77778e-7 * time_delta * (power - math.fsum(battery_power_list)))

    @staticmethod
    def _optimized_load_power(t, load_it):
        return math.fsum(
            map(
                lambda load: load.power_consumption
                if load.start_time <= 3600 * t.hour + 60 * t.minute + t.second < load.start_time + load.cycle_duration
                else 0,
                load_it
            )
        )

    def _cost_function(self, load_start_time: pd.Timestamp, load: StaggeredLoad,
                       power_production_df: pd.DataFrame, optimized_loads=()) -> float:
        init_battery_charge_tp = [battery.stored_energy for battery in self.battery_tp]
        t = pd.date_range(self.date, self.date + pd.DateOffset(days=1), freq="300S")
        cost = 0.0
        time_delta = 300

        if self.has_electrical_car():
            initial_car_charge = self._electrical_car_battery.stored_energy

            if self._electrical_car_battery.stored_energy >= self._electrical_car_battery.daily_required_energy:
                nb_intervals = 0

            else:
                nb_intervals = 96 - ((self._electrical_car_battery.daily_required_energy - self._electrical_car_battery.stored_energy)
                    / self._electrical_car_battery.max_power) // 300 + 1

            for i in range(96-nb_intervals):
                total_power = self.continuous_load_power() \
                              + self.timed_load_power(t[i]) \
                              + self._optimized_load_power(t[i], optimized_loads) \
                              + time_delta * load.power_consumption if load_start_time < t[i] < load_start_time + pd.Timedelta(seconds=load.cycle_duration) else 0 \
                              - power_production_df.loc[t[i]].values[2]
                cost += self._interval_cost_charge_car(t[i], time_delta, total_power)

            for i in range(96-nb_intervals, 96):
                total_power = self.continuous_load_power() \
                              + self.timed_load_power(t[i]) \
                              + self._optimized_load_power(t[i], optimized_loads) \
                              + time_delta * load.power_consumption if load_start_time < t[i] < load_start_time + pd.Timedelta(seconds=load.cycle_duration) else 0 \
                              + time_delta * 16500 \
                              - power_production_df.loc[t[i]].values[2]
                self._electrical_car_battery.stored_energy += 16500*time_delta
                cost += self._interval_cost(t[i], time_delta, total_power)

            for i in range(96, 222):
                total_power = self.continuous_load_power() \
                              + self.timed_load_power(t[i]) \
                              + self._optimized_load_power(t[i], optimized_loads) \
                              + time_delta * load.power_consumption if load_start_time < t[i] < load_start_time + pd.Timedelta(seconds=load.cycle_duration) else 0 \
                              - power_production_df.loc[t[i]].values[2]
                cost += self._interval_cost(t[i], time_delta, total_power)

            for i in range(222, 288):
                total_power = self.continuous_load_power() \
                              + self.timed_load_power(t[i]) \
                              + self._optimized_load_power(t[i], optimized_loads) \
                              + time_delta * load.power_consumption if load_start_time < t[i] < load_start_time + pd.Timedelta(seconds=load.cycle_duration) else 0 \
                              - power_production_df.loc[t[i]].values[2]
                cost += self._interval_cost_charge_car(t[i], time_delta, total_power)

            self._electrical_car_battery.stored_energy = initial_car_charge

        else:
            for i in range(len(t)):
                total_power = self.continuous_load_power() \
                              + self.timed_load_power(t[i]) \
                              + self._optimized_load_power(t[i], optimized_loads) \
                              + load.power_consumption if load_start_time < t[i] < load_start_time + pd.Timedelta(seconds=load.cycle_duration) else 0 \
                              - power_production_df.loc[t[i]].values[2]
                cost += self._interval_cost(t[i], time_delta, total_power)

        for i in range(len(init_battery_charge_tp)):
            self.battery_tp[i].stored_energy = init_battery_charge_tp[i]

        return cost

    def optimise(self, irradiance_df: pd.DataFrame, wind_speed_df: pd.DataFrame):
        sorted_load = sorted(self.staggered_load_list, key=lambda load: load.power_consumption * load.cycle_duration,
                             reverse=True)

        power_generation_df = pd.DataFrame(index=pd.date_range(self.date, self.date+pd.DateOffset(), freq="300S"))
        power_generation_df = power_generation_df.merge(irradiance_df, left_index=True, right_index=True)
        power_generation_df = power_generation_df.merge(wind_speed_df, left_index=True, right_index=True)
        power_generation_df.columns = ["Irradiance", "WindSpeed"]
        power_generation_df.index.name = "Timestamp"

        power_generation_df["AvailablePower"] = list(map(lambda ws, sp: self.wind_power_production(ws) + sp,
                                                         power_generation_df["WindSpeed"],
                                                         map(self.solar_power_production,
                                                             power_generation_df.index,
                                                             power_generation_df["Irradiance"]
                                                             )
                                                         )
                                                     )
        for n in range(len(self.staggered_load_list)):
            min_t_start = 0.0
            min_cost = math.inf
            for load_start_time in pd.date_range(pd.Timestamp(self.date), pd.Timestamp(self.date) + pd.Timedelta(seconds=86400-sorted_load[n].cycle_duration), freq="300S"):
                cost = self._cost_function(load_start_time, sorted_load[n], power_generation_df,
                                           sorted_load[:n])

                if cost < min_cost:
                    min_cost = cost
                    min_t_start = load_start_time

            sorted_load[n].start_time = min_t_start

        self._is_optimised = True

    def electricity_cost(self, t: pd.Timestamp, consumed_energy: float) -> float:
        """

        :param t:
        :param consumed_energy: energy in kWh
                                negative values means that energy was produced by self
        :return:

            peak:       8:00 - 20:00 on weekdays
            off-peak:   20:00 - 8:00 and weekends
        """
        if self.is_large_installation:
            if consumed_energy >= 0:
                return 0.24 * consumed_energy

            else:
                if t.hour < 8 or t.hour >= 20 or t.dayofweek >= 6:
                    return 0.036 * consumed_energy

                else:
                    return 0.052 * consumed_energy

        else:
            return 0.24 * consumed_energy

    def advance_time(self, irradiance_df: pd.DataFrame, wind_speed_df: pd.DataFrame) -> float:
        cost = 0.0
        time_delta = 300

        if self.has_electrical_car():
            t = [t for t in pd.date_range(self.date, self.date + pd.DateOffset(days=1), freq="300S")]

            for i in range(96):
                total_power = self.total_optimised_load_power(t[i]) - self.power_production(t[i], irradiance_df, wind_speed_df)
                cost += self._interval_cost_charge_car(t[i], time_delta, total_power)

            for i in range(96, 222):
                total_power = self.total_optimised_load_power(t[i]) - self.power_production(t[i], irradiance_df, wind_speed_df)
                cost += self._interval_cost(t[i], time_delta, total_power)

            for i in range(222, 288):
                total_power = self.total_optimised_load_power(t[i]) - self.power_production(t[i], irradiance_df, wind_speed_df)
                cost += self._interval_cost_charge_car(t[i], time_delta, total_power)
        else:
            cost = math.fsum(
                map(
                    lambda t: self._interval_cost(t, 300, self.total_optimised_load_power(t) - self.power_production(t, irradiance_df, wind_speed_df)),
                    pd.date_range(pd.Timestamp(self.date), pd.Timestamp(self.date) + pd.DateOffset(), freq="300S")
                )
            )

        self.timestamp += pd.DateOffset()
        self._is_optimised = False

        return cost

    def original_day_cost(self, irradiance_df: pd.DataFrame, wind_speed_df: pd.DataFrame):
        cost = 0.0
        time_delta = 300
        if self.has_electrical_car():
            t = [t for t in pd.date_range(pd.Timestamp(self.date), pd.Timestamp(self.date) + pd.DateOffset(days=1), freq="300S")]

            for i in range(96):
                total_power = self.total_original_load_power(t[i]) - self.power_production(t[i], irradiance_df, wind_speed_df)
                cost += self._interval_cost_charge_car(t[i], time_delta, total_power)

            for i in range(96, 222):
                total_power = self.total_original_load_power(t[i]) - self.power_production(t[i], irradiance_df, wind_speed_df)
                cost += self._interval_cost(t[i], time_delta, total_power)

            for i in range(222, 288):
                total_power = self.total_original_load_power(t[i]) - self.power_production(t[i], irradiance_df, wind_speed_df)
                cost += self._interval_cost_charge_car(t[i], time_delta, total_power)

        else:
            cost = math.fsum(
                map(
                    lambda t: self._interval_cost(t, 300, self.total_original_load_power(t) - self.power_production(t, irradiance_df, wind_speed_df)),
                    pd.date_range(pd.Timestamp(self.date), pd.Timestamp(self.date) + pd.DateOffset(), freq="300S")
                )
            )

        return cost