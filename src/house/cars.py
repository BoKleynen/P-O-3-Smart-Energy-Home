from abc import ABCMeta
from bisect import bisect


class Car(metaclass=ABCMeta):
    def __init__(self, price, year, year_first_registration_tax, fuel_consumption, fuel_capacity, co2_emissions: int,
                 fuel_type: str, euronorm: str, cylinder_capacity: int):
        self._price = price
        self._year = year
        self._year_first_registration_tax = year_first_registration_tax
        self._fuel_consumption = fuel_consumption
        self._fuel_capacity = fuel_capacity
        self._co2_emissions = co2_emissions
        self._fuel_type = fuel_type
        self._euronorm = euronorm
        self._cylinder_capacity = cylinder_capacity

    @property
    def price(self):
        return self._price

    @property
    def year(self):
        return self._year

    @property
    def year_first_registration_tax(self):
        return self._year_first_registration_tax

    @property
    def fuel_consumption(self):
        return self._fuel_consumption

    @property
    def fuel_capacity(self):
        return self._fuel_capacity

    @property
    def co2_emissions(self):
        return self._co2_emissions

    @property
    def fuel_type(self):
        return self._fuel_type

    @property
    def euronorm(self):
        return self._euronorm

    @property
    def cylinder_capacity(self):
        return self._cylinder_capacity

    def subsidy(self):
        ...

    def x_value(self):
        ...

    def f_value(self):
        ...

    def air_component(self):
        ...

    def age_correction(self):
        ...

    def biv(self):
        ...

    def vkb(self):
        ...

    def insurance(self):
        pass

    def maintenance_costs(self):
        pass
    

class ElectricalCar(Car):
    def __init__(self, price, year, year_first_registration_tax, fuel_consumption, fuel_capacity, co2_emissions=None,
                 fuel_type=None, euronorm=None, cylinder_capacity=None):
        super().__init__(price, year, year_first_registration_tax, fuel_consumption, fuel_capacity, co2_emissions,
                         fuel_type, euronorm, cylinder_capacity)

    @property
    def subsidy(self):
        # year : (price < 31000, 31000 <= price <= 40999, 41000 <= price <= 60999, 61000 < price)
        subsidy_map = {2016: (5000, 4500, 3000, 2500),
                       2017: (4000, 3500, 2500, 2000),
                       2018: (3000, 2500, 2000, 1500),
                       2019: (2000, 1500, 1500, 1000)}
        
        if super().price() < 31000:
            return subsidy_map[super().year()][0]
        
        elif 31000 <= super().price() <= 40999:
            return subsidy_map[super().year()][1]
        
        elif 41000 <= super().price() <= 60999:
            return subsidy_map[super().year()][2]
        
        else:
            return subsidy_map[super().year()][3]

    def biv(self):
        return 0

    def vkb(self):
        return 0


class PetrolCar(Car):
    def __init__(self, price, year, year_first_registration_tax, fuel_consumption, fuel_capacity, co2_emissions,
                 fuel_type, euronorm, cylinder_capacity):
        super().__init__(price, year, year_first_registration_tax, fuel_consumption, fuel_capacity, co2_emissions,
                         fuel_type, euronorm, cylinder_capacity)

    def subsidy(self):
        return 0

    def x_value(self):
        return 4.5 * (super().year - 2012)

    def f_value(self):
        if super().fuel_type == "lpg":
            return 0.88
        elif super().fuel_type == "natural_gas":
            return 0.93
        elif super().fuel_type == "natural_gas_and_gasoline":
            return 0.744
        else:
            return 1

    def air_component(self):
        if super().fuel_type == "diesel":
            if super().euronorm == "euro 0":
                return 2980.54
            elif super().euronorm == "euro 1":
                return 874.44
            elif super().euronorm == "euro 2":
                return 648.1
            elif super().euronorm == "euro 3":
                return 513.59
            elif super().euronorm == "euro 3 + soot filter" or super().euronorm == "euro 4":
                return 486.21
            elif super().euronorm == "euro 4 + soot filter" or super().euronorm == "euro 5":
                return 478.18
            else:
                return 472.69

        else:
            if super().euronorm == "euro 0":
                return 1185.47
            elif super().euronorm == "euro 1":
                return 530.16
            elif super().euronorm == "euro 2":
                return 158.53
            elif super().euronorm == "euro 3":
                return 99.45
            elif super().euronorm == "euro 4":
                return 23.87
            else:
                return 21.46

    def age_correction(self):
        nb_years_in_use = super().year - super().year_first_registration_tax
        return 1 - nb_years_in_use/10 if nb_years_in_use < 9 else 0.1

    def biv(self):
        """formula is only correct when the year_of_first_registration_tax is 2017 or higher"""
        # https://belastingen.vlaanderen.be/formule-berekenen-belasting-op-inverkeerstelling
        biv = (((super().co2_emissions * self.f_value() + self.x_value()) / 246) ** 6 * 4500 +
               self.air_component()) * self.age_correction()
        return round(biv, 2)

    def co2_factor(self):
        if super().co2_emissions <= 24:
            return -0.0030 * (122 - 24)
        elif 24 < super().co2_emissions <= 122:
            return -0.0030 * (122 - super().co2_emissions)
        elif 122 < super().co2_emissions <= 500:
            return 0.0030 * (super().co2_emissions-122)
        elif super().co2_emissions > 500:
            return 0.0030 * (500-122)

    def air_term(self):
        if super().fuel_type == "diesel":
            if super().euronorm == "euro 0":
                return 0.50
            elif super().euronorm == "euro 1":
                return 0.40
            elif super().euronorm == "euro 2":
                return 0.35
            elif super().euronorm == "euro 3":
                return 0.30
            elif super().euronorm == "euro 3 + soot filter" or super().euronorm == "euro 4":
                return 0.25
            elif super().euronorm == "euro 4 + soot filter" or super().euronorm == "euro 5":
                return 0.175
            elif super().euronorm == "euro 6":
                return 0.15

        else:
            if super().euronorm == "euro 0":
                return 0.30
            elif super().euronorm == "euro 1":
                return 0.10
            elif super().euronorm == "euro 2":
                return 0.05
            elif super().euronorm == "euro 3":
                return 0.00
            elif super().euronorm == "euro 4":
                return -0.125
            else:
                return -0.15

    def vkb(self):
        """this is only correct when the car is signed up after 01/01/2016"""

        opdeciem = 0.10

        breakpoints = [0.8, 1, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.1, 3.3, 3.5, 3.7, 4.0, 4.2]
        price = [80.52, 100.72, 145.73, 190.34, 235.36, 280.37, 324.85, 421.61, 518.36, 614.86, 711.61, 808.24, 1058.77,
                 1309.44, 1560.11, 1810.12, 2060.65]
        i = bisect(breakpoints, super().cylinder_capacity)
        ecoboni_ecomali = price[i] * (self.co2_factor() + self.air_term())
        vkb = price[i] + ecoboni_ecomali
        if vkb > 40:
            return round(vkb, 2)
        else:
            return round(40 + opdeciem, 2)


# TODO: verzekering, onderhoudskosten, ...
