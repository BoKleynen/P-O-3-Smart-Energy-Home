from abc import ABCMeta
from bisect import bisect


class Car(metaclass=ABCMeta):
    def __init__(self, price, year, fuel_consumption, fuel_capacity, leasing: bool, co2_emissions: int, fuel_type: str,
                 euronorm: str, cylinder_capacity: int):
        self.price = price
        self.year = year
        self.fuel_consumption = fuel_consumption
        self.fuel_capacity = fuel_capacity
        self.leasing = leasing
        self.co2_emissions = co2_emissions
        self.fuel_type = fuel_type
        self.euronorm = euronorm
        self.cylinder_capacity = cylinder_capacity
    
    def get_price(self):
        return self.price
    
    def get_year(self):
        return self.year
    
    def get_fuel_consumption(self):
        return self.fuel_consumption
    
    def get_fuel_capacity(self):
        return self.fuel_capacity
    
    def get_subsidy(self):
        ...

    def get_leasing(self):
        return self.leasing

    def get_co2_emissions(self):
        return self.co2_emissions

    def get_fuel_type(self):
        return self.fuel_type

    def get_euronorm(self):
        return self.euronorm

    def get_cylinder_capacity(self):
        return self.cylinder_capacity

    def get_x_value(self):
        ...

    def get_f_value(self):
        ...

    def get_air_component(self):
        ...

    def get_age_correction(self):
        ...

    def get_biv(self):
        ...

    def get_vkb(self):
        ...
    

class ElectricalCar(Car):
    def __init__(self, price, year, fuel_consumption, fuel_capacity, leasing, co2_emissions, fuel_type, euronorm, cylinder_capacity):
        super().__init__(price, year, fuel_consumption, fuel_capacity, leasing, co2_emissions, fuel_type, euronorm, cylinder_capacity)
    
    def get_subsidy(self):
        # year : (price < 31000, 31000 <= price <= 40999, 41000 <= price <= 60999, 61000 < price)
        subsidy_map = {2016: (5000, 4500, 3000, 2500),
                       2017: (4000, 3500, 2500, 2000),
                       2018: (3000, 2500, 2000, 1500),
                       2019: (2000, 1500, 1500, 1000)}
        
        if super().get_price() < 31000:
            return subsidy_map[super().get_year()][0]
        
        elif 31000 <= super().get_price() <= 40999:
            return subsidy_map[super().get_year()][1]
        
        elif 41000 <= super().get_price() <= 60999:
            return subsidy_map[super().get_year()][2]
        
        else:
            return subsidy_map[super().get_year()][3]

    def get_biv(self):
        return 0

    def get_vkb(self):
        return 0
        
class PetrolCar(Car):
    def __init__(self, price, year, fuel_consumption, fuel_capacity, leasing, co2_emissions, fuel_type, euronorm,
                 cylinder_capacity):
        super().__init__(price, year, fuel_consumption, fuel_capacity, leasing, co2_emissions, fuel_type, euronorm,
                         cylinder_capacity)

    def get_subsidy(self):
        return 0

    def get_x_value(self):
        current_year = 2017
        return 4.5 * (current_year - 2012)

    def get_f_value(self):
        if super().get_fuel_type() == "lpg":
            return 0.88
        elif super().get_fuel_type() == "natural_gas":
            return 0.93
        elif super().get_fuel_type() == "natural_gas_and_gasoline":
            return 0.744
        else:
            return 1

    def get_air_component(self):
        if super().get_fuel_type() == "diesel":
            if super().get_euronorm() == "euro 0":
                return 2980.54
            elif super().get_euronorm() == "euro 1":
                return 874.44
            elif super().get_euronorm() == "euro 2":
                return 648.1
            elif super().get_euronorm() == "euro 3":
                return 513.59
            elif super().get_euronorm() == "euro 3 + soot filter" or "euro 4":
                return 486.21
            elif super().get_euronorm() == "euro 4 + soot filter" or "euro 5":
                return 478.18
            else:
                return 472.69

        else:
            if super().get_euronorm() == "euro 0":
                return 1185.47
            elif super().get_euronorm() == "euro 1":
                return 530.16
            elif super().get_euronorm() == "euro 2" or "euro 3":
                return 158.53
            elif super().get_euronorm() == "euro 4":
                return 99.45
            elif super().get_euronorm() == "euro 5":
                return 23.87
            else:
                return 21.46

    def get_age_correction(self):
        current_year = 2017
        nb_years_in_use = (current_year - super().get_year())
        if nb_years_in_use < 1:
            return 1
        elif 1 < nb_years_in_use < 2:
            return 0.90
        elif 2 < nb_years_in_use < 3:
            return 0.80
        elif 3 < nb_years_in_use < 4:
            return 0.70
        elif 4 < nb_years_in_use < 5:
            return 0.60
        elif 5 < nb_years_in_use < 6:
            return 0.50
        elif 6 < nb_years_in_use < 7:
            return 0.40
        elif 7 < nb_years_in_use < 8:
            return 0.30
        elif 8 < nb_years_in_use < 9:
            return 0.20
        else:
            return 0.10

    def get_biv(self):
        if super().get_leasing() is True:
            pass
        else:
            # https://belastingen.vlaanderen.be/formule-berekenen-belasting-op-inverkeerstelling
            return round((((super().get_co2_emissions() * self.get_f_value() + self.get_x_value()) / 246) ** 6
                    * 4500 + self.get_air_component()) * self.get_age_correction(), 2)

    def co2_factor(self):
        if super().get_co2_emissions() <= 24:
            return -0.0030 * (122 - 24)
        elif 24 < super().get_co2_emissions() <= 122:
            return -0.0030 * (122 - super().get_co2_emissions())
        elif 122 < super().get_co2_emissions() <= 500:
            return 0.0030 * (super().get_co2_emissions()-122)
        elif super().get_co2_emissions() > 500:
            return 0.0030 * (500-122)

    def air_term(self):
        if super().get_fuel_type() == "diesel":
            if super().get_euronorm() == "euro 0":
                return 0.50
            elif super().get_euronorm() == "euro 1":
                return 0.40
            elif super().get_euronorm() == "euro 2":
                return 0.35
            elif super().get_euronorm() == "euro 3":
                return 0.30
            elif super().get_euronorm() == "euro 3 + soot filter" or "euro 4":
                return 0.25
            elif super().get_euronorm() == "euro 4 + soot filter" or "euro 5":
                return 0.175
            elif super().get_euronorm() == "euro 6":
                return 0.15

        else:
            if super().get_euronorm() == "euro 0":
                return 0.30
            elif super().get_euronorm() == "euro 1":
                return 0.10
            elif super().get_euronorm() == "euro 2":
                return 0.05
            elif super().get_euronorm() == "euro 3":
                return 0.00
            elif super().get_euronorm() == "euro 4":
                return -0.125
            else:
                return -0.15

    def get_vkb(self):
        """this is only correct when the car is signed up after 01/01/2016"""

        opdeciem = 0.10

        breakpoints = [0.8, 1, 1.2, 1.4, 1.6, 1.8, 1.9, 2.0, 2.2, 2.4, 2.6, 2.8, 3.1, 3.3, 3.5, 3.7, 4.0, 4.2]
        price = [80.52, 100.72, 145.73, 190.34, 235.36, 280.37, 324.85, 421.61, 518.36, 614.86, 711.61, 808.24, 1058.77,
                 1309.44, 1560.11, 1810.12, 2060.65]
        i = bisect(breakpoints, super().get_cylinder_capacity())
        vkb = price[i] * (1 + self.co2_factor() + self.air_term() + opdeciem)
        if vkb > 40:
            return round(vkb, 2)
        else:
            return round(40 + opdeciem, 2)


#TODO: verzekering, onderhoudskosten, ...
