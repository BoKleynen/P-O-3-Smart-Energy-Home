from datetime import datetime, date, time, timedelta
from house.House import House
from util.Util import date_range


class Simulation:
    def __init__(self, house: House):
        self.house = house

    def simulate(self, start: date, end: date):
        for day in date_range(start, end):
            pass
