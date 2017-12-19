from tkinter import *
from math import pi
from house.production.wind_mill import *
from house.production.solar_panel import *
from house.loads import *
from house.battery import *
from house.house import *
from house.battery import *
from house.cars import *
from simulation.simulation import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

solar_panel_1 = (SolarPanel(285.0, 0.64, 0, 0.87, 1.540539, 20),)  # South
solar_panel_2 = (SolarPanel(285.0, 0.17, -pi/2, 0.87, 1.540539, int(20/2)),
                 SolarPanel(285.0, 0.17, pi/2, 0.87, 1.540539, int(20/2)+1))  # East-West
windmill = None

# Make output window
output = Tk()
output.title("Results of the simulation")
output.configure(background="white")

output.attributes("-fullscreen", True)
output.bind("<Escape>", lambda x: output.attributes("-fullscreen", False))
output.bind("<F11>", lambda x: output.attributes("-fullscreen", False))

button1 = Button(output, text='Sluit venster', width=25, height=2, relief=SOLID, background="white",
                 activebackground="white", command=lambda: output.destroy())
button1.pack()

# Show graphs
start = pd.Timestamp("2016-05-24 00:00:00")
end = pd.Timestamp("2016-05-24 23:55:00")
# end = pd.Timestamp("2017-04-21 23:55:00")
times = pd.date_range(start, end, freq="300S")


if solar_panel_1 and solar_panel_2 is not None:
    irradiance_df = pd.read_csv(
        filepath_or_buffer="C:\\Users\\Lander\\Documents\\KULeuven\\2e bachelor\\semester 1\\P&O 3\\P-O-3-Smart-Energy-Home\\data\\Irradiance.csv",
        header=0, index_col="Date/Time", dtype={"watts-per-meter-sq": float}, parse_dates=["Date/Time"])

    data_production_solar_panel_2 = [solar_panel_2[0].power_production(t, 1) +
                                     solar_panel_2[1].power_production(t, 1)
                                     for t in pd.date_range(start, end, freq="300S")]

    data_production_solar_panel_1 = [solar_panel_1[0].power_production(t, 1)
                                     for t in pd.date_range(start, end, freq="300S")]
if windmill is not None:
    wind_speed_df = pd.read_csv(
        filepath_or_buffer="C:\\Users\\Lander\\Documents\\KULeuven\\2e bachelor\\semester 1\\P&O 3\\P-O-3-Smart-Energy-Home\\data\\wind_speed.csv",
        header=0, index_col="Date/Time", dtype={"meters-per-second": float}, parse_dates=["Date/Time"])
    data_production_windmill = [windmill.power_production(wind_speed_df.loc[t].values[0])
                                for t in pd.date_range(start, end, freq="300")]

fig = Figure(figsize=(15, 8))
if windmill is not None or solar_panel_1 or solar_panel_2 is not None:
    a = fig.add_subplot(111)
    if windmill is not None:
        a.plot_date(times, data_production_windmill, color="red", linestyle="solid", linewidth=2, marker=None)
    if solar_panel_1 and solar_panel_2 is not None:
        a.plot_date(times, data_production_solar_panel_1, color="blue", linestyle="solid", linewidth=2, marker=None)
        a.plot_date(times, data_production_solar_panel_2, color="red", linestyle="solid", linewidth=2, marker=None)
    a.xaxis.set_major_formatter(DateFormatter("%H: %M"))
    # a.xaxis.set_major_formatter(DateFormatter("%d/%m/%y"))
    a.set_title("Titel", fontsize=16)
    a.set_ylabel("vermogen [W]", fontsize=14)
    a.set_xlabel("tijd [uur: minuten]", fontsize=14)
    # a.set_xlabel("tijd [dag/maand/jaar]", fontsize=14)

canvas = FigureCanvasTkAgg(fig, master=output)
canvas.get_tk_widget().pack()
canvas.draw()

output.mainloop()
