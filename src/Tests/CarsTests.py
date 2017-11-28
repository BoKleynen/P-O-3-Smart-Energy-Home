from src.house.Cars import *

# price, year, year_first_registration_tax, fuel_consumption, fuel_capacity, co2_emissions: int, fuel_type: str,
# euronorm: str, cylinder_capacity: int

# Test for Mercedes ...
#PetrolCar(price, year, fuel_consumption, fuel_capacity, leasing, co2_emissions, fuel_type, euronorm, cylinder_capacity)

# Test for Tesla Model S
#tesla_model_s = ElectricalCar()

# Test for Renault Clio
renault_clio = PetrolCar(15000, 2017, 2010, 5.0, 50.0, 139, "gasoline", "euro 4", 1.1)
print("biv: ", renault_clio.get_biv())  # bekomt een juiste waarde
print("vkb: ", renault_clio.get_vkb())  # bekomt een foute waarde
