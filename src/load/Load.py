from abc import ABCMeta


class Load(metaclass=ABCMeta):
    def __init__(self, power):
        self.power = power

    def get_power(self):
        return self.power

