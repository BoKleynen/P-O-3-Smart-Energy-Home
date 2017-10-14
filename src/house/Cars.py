from abc import ABCMeta


class Car(metaclass=ABCMeta):
    def __init__(self, price, year, fuel_consumption, fuel_capacity):
        self.price = price
        self.year = year
        self.fuel_consumption = fuel_consumption
        self.fuel_capacity = fuel_capacity
    
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
    

class ElectricalCar(Car):
    def __init__(self, price, year, fuel_consumption, fuel_capacity):
        super().__init__(price, year, fuel_consumption, fuel_capacity)
    
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
        
        
class PetrolCar(Car):
    def __init__(self, price, year, fuel_consumption, fuel_capacity):
        super().__init__(price, year, fuel_consumption, fuel_capacity)

    def get_subsidy(self):
        return 0
