from . import ElectricalAppliance


class WashingMachine(ElectricalAppliance.ElectricalAppliance):
    def __init__(self, power):
        super().__init__(power)
