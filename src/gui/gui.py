from tkinter import *
from math import pi
import pyximport
pyximport.install()
from cython_src.power_generators import *
from cython_src.loads import *
from cython_src.battery import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter


def stop_fullscreen_1(event):
    """stop fullscreen mode"""
    root.attributes("-fullscreen", False)


def start_fullscreen_1(event):
    """start fullscreen mode"""
    root.attributes("-fullscreen", True)


def slider_sun_panel(option):
    global nb_sun_panel

    if option == "geen zonnepanelen":
        nb_sun_panel.place_forget()
    else:
        nb_sun_panel.place(x=55, y=80)


def slider_electric_car(option):
    global nb_car
    nb_car.place(x=530, y=80)


def show_wind_turbine_and_battery(option):
    global battery1

    if option == "windmolen en thuisbatterij":
        battery1.place(x=screen_width / 2 - drawing_new_house_width / 2 - 250,
                      y=screen_height / 2 - drawing_new_house_height / 2 + 450)
        wind_turbine.place(x=screen_width / 2 - drawing_new_house_width / 2 - 265,
                           y=screen_height / 2 - drawing_new_house_height / 2 - 90)
    else:
        battery1.place_forget()
        wind_turbine.place_forget()


def show_sun_panels(option):
    pass


def show_car(option):
    global Tesla_model_S

    if option == "elektrische wagen":
        Mercedes.place_forget()
        Tesla_model_S.place(x=screen_width / 2 - drawing_new_house_width / 2 + 500,
                            y=screen_height / 2 - drawing_new_house_height / 2 + 355)
    else:
        Tesla_model_S.place_forget()
        Mercedes.place(x=screen_width / 2 - drawing_new_house_width / 2 + 500,
                       y=screen_height / 2 - drawing_new_house_height / 2 + 355)


def show_house(option):
    global new_house
    global old_house

    if option == "oost-west-georiënteerd":
        old_house.place_forget()
        new_house.place(x=screen_width / 2 - drawing_new_house_width / 2,
                        y=screen_height / 2 - drawing_new_house_height / 2)
    else:
        new_house.place_forget()
        old_house.place(x=screen_width / 2 - drawing_new_house_width / 2,
                        y=screen_height / 2 - drawing_new_house_height / 2)


def combine_func(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)

    return combined_func


def start_simulation():
    sun_panel = variable_sun_panel.get()
    nb_sun_panels = nb_sun_panel.get()
    windmill_battery = variable_wind_turbine_and_battery.get()
    cars = variable_electric_car.get()
    nb_cars = nb_car.get()
    house = variable_house.get()

    fridge = ContinuousLoad(90)
    freezer = ContinuousLoad(90)
    led_tv = TimedLoad(60, time(hour=20, minute=30), 3600, pd.DateOffset())
    stove = TimedLoad(5250, time(hour=17, minute=30), 900, pd.DateOffset())
    dishwasher = StaggeredLoad(900, time(hour=7), 9600, time_delta=pd.DateOffset())
    washing_machine = StaggeredLoad(1000, time(hour=21), 4800, time_delta=pd.DateOffset())
    tumble_dryer = StaggeredLoad(2600, time(hour=21), 5400, time_delta=pd.DateOffset())
    led_lamps = TimedLoad(240, time(hour=20), 18000, pd.DateOffset())
    central_heating_1 = TimedLoad(2400, time(hour=6, minute=30), 9000, time_delta=pd.DateOffset())
    central_heating_2 = TimedLoad(2400, time(hour=18), 9000, time_delta=pd.DateOffset())
    computer = TimedLoad(800, time(hour=21), 7200, pd.DateOffset())
    microwave = TimedLoad(1500, time(hour=18), 600, pd.DateOffset())
    hairdryer = TimedLoad(300, time(hour=7, minute=30), 600, pd.DateOffset())
    hood = TimedLoad(150, time(hour=17, minute=30), 900, pd.DateOffset())
    boiler = StaggeredLoad(2000, time(hour=0), 16200, time_delta=pd.DateOffset())
    swimming_pool_pump = StaggeredLoad(1100, time(hour=0), 43200, time_delta=pd.DateOffset())
    heat_pump_boiler = StaggeredLoad(700, time(hour=0), 16200, time_delta=pd.DateOffset())
    oven = TimedLoad(2500, time(hour=17, minute=30), 900, pd.DateOffset())

    if cars == "elektrische wagen":
        car = nb_cars*(ElectricalCar(84100, 2017, 2017, 0, 21.9, 75, 75),)
        car_battery = CarBattery(75, 16500)
    elif cars == "brandstofwagen":
        car = nb_cars*(PetrolCar(67276, 2017, 2017, 7.6, 66, 176, "gasoline", "euro) 6", 3.498),)
        car_battery = None
    else:
        raise Exception("you have to make a chose.1")

    if sun_panel == "zonnepanelen":
        if house == "zuid georiënteerd":
            solar_panel = (SolarPanel(285.0, 0.64, pi, 0.87, 1.540539, nb_sun_panels),)
        elif house == "oost-west-georiënteerd":
            if nb_sun_panels != 1:
                solar_panel = (SolarPanel(285.0, 0.17, -pi/2, 0.87, 1.540539, int(nb_sun_panels/2)),
                               SolarPanel(285.0, 0.17, pi/2, 0.87, 1.540539, int(nb_sun_panels/2)+1))
            else:
                solar_panel = (SolarPanel(285.0, 0.17, pi/2, 0.87, 1.540539, nb_sun_panels), )
        else:
            raise Exception("you have to make a chose.2")
    elif sun_panel == "geen zonnepanelen":
        solar_panel = ()
    else:
        raise Exception("you have to make a chose.3")

    if windmill_battery == "windmolen en thuisbatterij":
        windmill = (Windmill(9.448223734, 2.5, 12.75190283),)
        battery = (Battery(13.5, 5),)
    elif windmill_battery == "geen windmolen en geen thuisbatterij":
        windmill = ()
        battery = ()
    else:
        raise Exception("you have to make a chose.4")

    loads = [freezer, fridge, led_tv, stove, dishwasher, washing_machine, tumble_dryer, led_lamps, central_heating_1,
             central_heating_2, computer, microwave, hairdryer, hood, boiler]
    house = House(loads, solar_panel_tp=solar_panel, windmill_tp=windmill, battery_tp=battery, car_battery=car_battery,
                  timestamp=pd.Timestamp("2016-05-24 00:00"))

    simulation = Simulation(house)
    cost_optimised = round(simulation.simulate_optimise(pd.Timestamp("2016-05-24 00:00:00"),
                                                        pd.Timestamp("2016-05-24 23:55:00")), 2)
    cost_normal = round(simulation.simulate_original(pd.Timestamp("2016-05-24 00:00:00"),
                                                     pd.Timestamp("2016-05-24 23:55:00")), 2)
    create_output_screen(house, cost_optimised, cost_normal, solar_panel[0] if house.has_solar_panel() else None,
                         windmill[0] if house.has_windmill() else None)


def create_output_screen(house, amount_optimised, amount_normal, solar_panel, windmill):
    amount_optimised = str(amount_optimised)
    amount_normal = str(amount_normal)

    # Make output window
    output = Tk()
    output.title("Results of the simulation_scenarios")
    output.configure(background="white")

    output.attributes("-fullscreen", True)
    output.bind("<Escape>", lambda x: output.attributes("-fullscreen", False))
    output.bind("<F11>", lambda x: output.attributes("-fullscreen", False))

    button1 = Button(output, text='Sluit venster', width=25, height=2, relief=SOLID, background="white",
                     activebackground="white", command=lambda: output.destroy())
    button1.pack()

    # Show results from the cost calculations
    w1 = Label(output, text="De simulatie is uitgevoerd voor de volgende dag: 24 mei 2016 \n"
                            "Te betalen bedrag aan elektriciteit met optimalisatie: €"+amount_optimised,
               background="white", font=("Ariel", 15))
    w3 = Label(output, text="Te betalen bedrag aan elektriciteit zonder optimalisatie: €"+amount_normal,
               background="white", font=("Ariel", 15))
    w1.pack()
    w3.pack()

    # Show graphs
    start = pd.Timestamp("2016-05-24 00:00:00")
    end = pd.Timestamp("2016-05-24 23:55:00")
    times = pd.date_range(start, end, freq="300S")
    house._is_optimised = True

    if solar_panel is not None:
        irradiance_df = pd.read_csv(filepath_or_buffer="C:\\Users\\Lander\\Documents\\KULeuven\\2e bachelor\\semester 1\\P&O 3\\P-O-3-Smart-Energy-Home\\data\\Irradiance.csv",
                                    header=0, index_col="Date/Time", dtype={"watts-per-meter-sq": float}, parse_dates=["Date/Time"])
        data_production_solar_panel = [solar_panel.power_production(t, irradiance_df.loc[t].values[0])
                                       for t in pd.date_range(start, end, freq="300S")]
    if windmill is not None:
        wind_speed_df = pd.read_csv(filepath_or_buffer="C:\\Users\\Lander\\Documents\\KULeuven\\2e bachelor\\semester 1\\P&O 3\\P-O-3-Smart-Energy-Home\\data\\wind_speed.csv",
                                    header=0, index_col="Date/Time", dtype={"meters-per-second": float}, parse_dates=["Date/Time"])
        data_production_windmill = [windmill.power_production(wind_speed_df.loc[t].values[0])
                                    for t in pd.date_range(start, end, freq="300S")]

    data_consumption = [house.optimised_staggered_load_power(t) for t in times]

    fig = Figure(figsize=(15, 8))
    if windmill is not None or solar_panel is not None:
        a = fig.add_subplot(121)
        if windmill is not None:
            a.plot_date(times, data_production_windmill, color="red", linestyle="solid", linewidth=2, marker=None)
        if solar_panel is not None:
            a.plot_date(times, data_production_solar_panel, color="blue", linestyle="solid", linewidth=2, marker=None)
        a.xaxis.set_major_formatter(DateFormatter("%H: %M"))
        a.set_title("elektriciteitsproductie door windmolen (rood) en zonnepanelen (blauw)", fontsize=16)
        a.set_ylabel("vermogen [W]", fontsize=14)
        a.set_xlabel("tijd [uur: minuten]", fontsize=14)
    b = fig.add_subplot(122)
    b.plot_date(times, data_consumption, color="blue", linestyle="solid", linewidth=2, marker=None)
    b.xaxis.set_major_formatter(DateFormatter("%H:%M"))
    b.set_title("elektriciteitsverbruik", fontsize=16)
    b.set_ylabel("vermogen [W]", fontsize=14)
    b.set_xlabel("tijd [uur:min]", fontsize=14)

    canvas = FigureCanvasTkAgg(fig, master=output)
    canvas.get_tk_widget().pack()
    canvas.draw()


# Make the input window
root = Tk()
root.title("GUI Smart Energy House")
root.configure(background='white')

# Set input screen to fullscreen mode
root.attributes("-fullscreen", True)
root.bind("<Escape>", stop_fullscreen_1)
root.bind("<F11>", start_fullscreen_1)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Make image of the new house
drawing_new_house = PhotoImage(file="NewHouse.png")
drawing_new_house_width = drawing_new_house.width()
drawing_new_house_height = drawing_new_house.height()
new_house = Label(root, image=drawing_new_house, background="white")

# Make image of the old house
drawing_old_house = PhotoImage(file="OldHouse.png")
old_house = Label(root, image=drawing_old_house, background="white")

# Make image of the battery
drawing_battery = PhotoImage(file="battery.png")
drawing_battery = drawing_battery.subsample(3, 3)
battery1 = Label(root, image=drawing_battery, background="white")

# Make image of the Tesla Model S
drawing_Tesla_model_S = PhotoImage(file="TeslaModelS.png")
drawing_Tesla_model_S = drawing_Tesla_model_S.subsample(2, 2)
Tesla_model_S = Label(root, image=drawing_Tesla_model_S, background="white")

# Make image of the Mercedes
drawing_Mercedes = PhotoImage(file="Mercedes.png")
Mercedes = Label(root, image=drawing_Mercedes, background="white")

# Make image of the wind turbine
drawing_wind_turbine = PhotoImage(file="WindTurbine.png")
wind_turbine = Label(root, image=drawing_wind_turbine, background="white")

# make image of the logo
drawing_logo = PhotoImage(file="logo.png")
drawing_logo_width = drawing_logo.width()
drawing_logo_height = drawing_logo.height()
logo = Label(root, image=drawing_logo, borderwidth=0)
logo.place(x=screen_width-drawing_logo_width-10, y=10)

# make the optionmenu's to chose your input
variable_sun_panel = StringVar(root)
variable_sun_panel.set("maak uw keuze")
sun_panel_menu = OptionMenu(root, variable_sun_panel, "zonnepanelen", "geen zonnepanelen",
                            command=combine_func(slider_sun_panel, show_sun_panels))
sun_panel_menu.configure(width=35, relief=SOLID, background="white", activebackground="white",
                         highlightbackground="white")
sun_panel_menu.place(x=10, y=50)

variable_wind_turbine_and_battery = StringVar(root)
variable_wind_turbine_and_battery.set("maak uw keuze")
wind_turbine_and_battery_menu = OptionMenu(root, variable_wind_turbine_and_battery, "windmolen en thuisbatterij",
                                           "geen windmolen en geen thuisbatterij", command=show_wind_turbine_and_battery)
wind_turbine_and_battery_menu.configure(width=35, relief=SOLID, background="white", activebackground="white",
                                        highlightbackground="white")
wind_turbine_and_battery_menu.place(x=270, y=50)

variable_electric_car = StringVar(root)
variable_electric_car.set("maak uw keuze")
electric_car_menu = OptionMenu(root, variable_electric_car, "elektrische wagen", "brandstofwagen",
                               command=combine_func(show_car, slider_electric_car))
electric_car_menu.configure(width=35, relief=SOLID, background="white", activebackground="white",
                            highlightbackground="white")
electric_car_menu.place(x=530, y=50)

variable_house = StringVar(root)
variable_house.set("maak uw keuze")
house_menu = OptionMenu(root, variable_house, "oost-west-georiënteerd", "zuid georiënteerd", command=show_house)
house_menu.configure(width=35, relief=SOLID, background="white", activebackground="white", highlightbackground="white")
house_menu.place(x=790, y=50)

# Make sliders to select number of sun panels and cars
nb_sun_panel = Scale(root, from_=1, to=20, orient=HORIZONTAL, background="white", borderwidth=1,
                     sliderrelief=FLAT, troughcolor="black", highlightbackground="white")

nb_car = Scale(root, from_=1, to=3, orient=HORIZONTAL, background="white", borderwidth=1, sliderrelief=FLAT,
               troughcolor="black", highlightbackground="white")

# Create a button to start the simulation_scenarios
button = Button(root, text='Start simulatie', width=25, height=5, relief=SOLID, background="white",
                activebackground="white", command=start_simulation)
button.place(x=screen_width/2-90, y=screen_height-100)

root.mainloop()
