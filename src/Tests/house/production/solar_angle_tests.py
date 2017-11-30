from house.production.solar_panel import SolarPanel
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import time

from matplotlib import dates
from datetime import date, datetime, timedelta

start = pd.Timestamp("2016-05-24 00:00")
end = pd.Timestamp("2017-04-21 23:55")
time_index = pd.date_range(start, end, freq="300S")

df = pd.DataFrame(index=time_index)

print(df)