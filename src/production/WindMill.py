from scipy.integrate import quad
import math


class Windmill:
    def __init__(self, radius):
        self.radius = radius

    @staticmethod
    def power_production(v, A):
        return 0.163 * A * v
    
    def get_produced_energy(self, v, start, end):
        return quad(Windmill.power_production(v, math.pi * pow(self.radius, 2)), start, end)
