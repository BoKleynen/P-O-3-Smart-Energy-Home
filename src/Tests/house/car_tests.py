from src.house.Cars import *


# Test for Mercedes E400 (http://www.mercedes-fiscalculator.be/nl)
mercedes_e_400 = PetrolCar(67276, 2017, 2017, 0, 7.6, 66, 176, "gasoline", "euro 6", 3.498)
assert mercedes_e_400.biv() == 1263.58
assert mercedes_e_400.vkb() == 1578.83
assert mercedes_e_400.fuel_costs(15500) == 1825.90

# Test for Tesla Model S 75
tesla_model_s_75 = ElectricalCar(84100, 2017, 2017, 0, 21.9, 75, 75)
assert tesla_model_s_75.biv() == 0
assert tesla_model_s_75.vkb() == 0
assert tesla_model_s_75.fuel_costs(15500) == 916.51

# Test for Renault Clio
renault_clio = PetrolCar(15000, 2017, 2010, 0, 5.0, 50.0, 139, "gasoline", "euro 4", 1.149)
assert renault_clio.biv() == 115.24
assert renault_clio.vkb() == 134.95
