from . import ElectricalAppliance


class DishWasher(ElectricalAppliance.ElectricalAppliance):
    def __init__(self, power):
        super().__init__(power)