import simulation.HouseSimulation
from house.Loads import *
from house.House import *


load1 = TimedLoad(lambda t: .5, 1800, 3600)
load2 = TimedLoad(lambda t: 0.5, 28000, 3600)
load3 = TimedLoad(lambda t: 1, 72001, 1000)

house = House([load1, load2, load3])

house.optimise()