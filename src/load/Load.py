from abc import ABCMeta


"""
Base class for modelling all the loads in a house
"""


class Load(metaclass=ABCMeta):
    def __init__(self, power):
        self.power = power

    def get_power(self):
        return self.power

