from house

# Test for Mercedes ...
PetrolCar(price, year, fuel_consumption, fuel_capacity, leasing, co2_emissions, fuel_type, euronorm, cylinder_capacity)

# Test for Tesla Model S
tesla_model_s = ElectricalCar()

# Test for Renault Clio
renault_clio = PetrolCar(15000, 2007, 5.0, 50.0, False, 139, "gasoline", "euro 4", 1.1)
print("biv: ", renault_clio.get_biv())
print("vkb: ", renault_clio.get_vkb())