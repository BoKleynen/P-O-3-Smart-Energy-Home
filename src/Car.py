from abc import ABCMeta


class Car(metaclass=ABCMeta):
    def __init__(self, price, year, fuel_consumption):
        self.price = price
        self.year = year
        self.fuel_consumption = fuel_consumption
    
    def get_price(self):
        return self.price

    def get_year(self):
        return self.year
    
    def get_fuel_consumption(self):
        return self.fuel_consumption
    
    def get_subsidy(self):
        ...


class ElectricalCar(Car):
    def __init__(self, price, year):
        Car.__init__(self, price, year)
    
    def get_subsidy(self):
        # year : (price < 31000, 31000 <= price <= 40999, 41000 <= price <= 60999, 61000 < price)
        subsidy_map = {2016: (5000, 4500, 3000, 2500),
                       2017: (4000, 3500, 2500, 2000),
                       2018: (3000, 2500, 2000, 1500),
                       2019: (2000, 1500, 1500, 1000)}
        
        if Car.get_price(self) < 31000:
            return subsidy_map[Car.get_year(self)][0]
        
        elif 31000 <= Car.get_price(self) <= 40999:
            return subsidy_map[Car.get_year(self)][1]
        
        elif 41000 <= Car.get_price(self) <= 60999:
            return subsidy_map[Car.get_year(self)][2]
        
        else:
            return subsidy_map[Car.get_year(self)][3]


class PetrolCar(Car):
    def __init__(self, price, year):
        Car.__init__(self, price, year)

    def get_subsidy(self):
        return 0
