from src.house.Cars import *

# price, year, year_first_registration_tax, fuel_consumption, fuel_capacity, co2_emissions: int, fuel_type: str,
# euronorm: str, cylinder_capacity: int

# Test for Mercedes E250 (http://www.mercedes-fiscalculator.be/nl)
mercedes_e_250 = PetrolCar(49973, 2017, 2017, 6.1, 66, 141, "benzine", "euro 6", 2.143)
assert mercedes_e_250.biv() == 409.35
assert mercedes_e_250.vkb() == 382.40

# Test for Tesla Model S 75
tesla_model_s_75 = ElectricalCar(86100, 2017, 2017, 0.219, 75)
assert tesla_model_s_75.biv() == 0
assert tesla_model_s_75.vkb() == 0

# Test for Renault Clio
renault_clio = PetrolCar(15000, 2017, 2010, 5.0, 50.0, 139, "gasoline", "euro 4", 1.149)
assert renault_clio.biv() == 115.24
assert renault_clio.vkb() == 134.95
