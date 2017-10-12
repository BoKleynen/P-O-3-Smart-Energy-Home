from abc import ABCMeta


"""
Base class for modelling all the loads in a house
"""


class Load(metaclass=ABCMeta):
    """
    Power_consumption: power consumed per unit time in watts
    """
    def __init__(self, power_consumption):
        self.power_consumption = power_consumption
