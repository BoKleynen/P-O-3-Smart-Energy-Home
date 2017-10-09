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
