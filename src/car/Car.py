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
