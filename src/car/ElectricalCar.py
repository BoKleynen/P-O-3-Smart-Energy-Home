from . import Car


class ElectricalCar(Car.Car):
    def __init__(self, price, year, fuel_consumption):
        super().__init__(price, year, fuel_consumption)
    
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