from . import Car


class PetrolCar(Car.Car):
    def __init__(self, price, year, fuel_consumption, fuel_capacity):
        super().__init__(price, year, fuel_consumption, fuel_capacity)

    def get_subsidy(self):
        return 0
