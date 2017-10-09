from . import Car


class PetrolCar(Car.Car):
    def __init__(self, price, year, fuel_consumption):
        super().__init__(price, year, fuel_consumption)

    def get_subsidy(self):
        return 0
