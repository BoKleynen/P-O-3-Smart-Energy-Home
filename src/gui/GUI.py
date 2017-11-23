from tkinter import *


def stop_fullscreen(event):
    """stop fullscreen mode"""
    root.attributes("-fullscreen", False)


def start_fullscreen(event):
    """start fullscreen mode"""
    root.attributes("-fullscreen", True)


def slider_sun_panel(option):
    global nb_sun_panel

    if option == "geen zonnepanelen":
        nb_sun_panel.place_forget()
    else:
        nb_sun_panel.place(x=55, y=80)


def slider_electric_car(option):
    global nb_electric_car
    nb_electric_car.place(x=530, y=80)


def show_wind_turbine_and_battery(option):
    global battery

    if option == "wel windmolen en thuisbatterij":
        battery.place(x=screen_width / 2 - drawing_new_house_width / 2 - 250,
                      y=screen_height / 2 - drawing_new_house_height / 2 + 450)
        wind_turbine.place(x=screen_width / 2 - drawing_new_house_width / 2 - 265,
                           y=screen_height / 2 - drawing_new_house_height / 2 - 90)
    else:
        battery.place_forget()
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

    if option == "nieuwbouw":
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


def start_simulation(option):
    pass


# Make the input screen
root = Tk()
root.title("GUI Smart Energy House")
root.iconbitmap(default="logo.ico")
root.configure(background='white')

# Set input screen to fullscreen mode
root.attributes("-fullscreen", True)
root.bind("<Escape>", stop_fullscreen)
root.bind("<F11>", start_fullscreen)
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
battery = Label(root, image=drawing_battery, background="white")

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

# make the optionmenus to chose your input
variable_sun_panel = StringVar(root)
variable_sun_panel.set("maak u keuze")
sun_panel_menu = OptionMenu(root, variable_sun_panel, "wel zonnepanelen", "geen zonnepanelen",
                            command=combine_func(slider_sun_panel, show_sun_panels))
sun_panel_menu.configure(width=30, relief=SOLID, background="white", activebackground="white",
                         highlightbackground="white")
sun_panel_menu.place(x=10, y=50)

variable_wind_turbine_and_battery = StringVar(root)
variable_wind_turbine_and_battery.set("maak u keuze")
wind_turbine_and_battery_menu = OptionMenu(root, variable_wind_turbine_and_battery, "wel windmolen en thuisbatterij",
                                           "geen windmolen en thuisbatterij", command=show_wind_turbine_and_battery)
wind_turbine_and_battery_menu.configure(width=30, relief=SOLID, background="white", activebackground="white",
                                        highlightbackground="white")
wind_turbine_and_battery_menu.place(x=240, y=50)

variable_electric_car = StringVar(root)
variable_electric_car.set("maak u keuze")
electric_car_menu = OptionMenu(root, variable_electric_car, "elektrische wagen", "brandstof wagen",
                               command=combine_func(show_car, slider_electric_car))
electric_car_menu.configure(width=30, relief=SOLID, background="white", activebackground="white",
                            highlightbackground="white")
electric_car_menu.place(x=470, y=50)

variable_house = StringVar(root)
variable_house.set("maak u keuze")
house_menu = OptionMenu(root, variable_house, "nieuwbouw", "bestaand huis", command=show_house)
house_menu.configure(width=30, relief=SOLID, background="white", activebackground="white", highlightbackground="white")
house_menu.place(x=700, y=50)

# Make sliders to select number of sun panels and cars
nb_sun_panel = Scale(root, from_=1, to=10, orient=HORIZONTAL, background="white", borderwidth=1,
                     sliderrelief=FLAT, troughcolor="black", highlightbackground="white")

nb_electric_car = Scale(root, from_=1, to=3, orient=HORIZONTAL, background="white", borderwidth=1, sliderrelief=FLAT,
                        troughcolor="black", highlightbackground="white")

# Create a button to start the simulation
button = Button(root, text='Start simulatie', width=25, height=5, relief=SOLID, background="white",
                activebackground="white", command=start_simulation)
button.place(x=screen_width/2-90, y=screen_height-100)

root.mainloop()

# TODO:
# - al dan niet tonen van de zonnepanelen
# - outputscreen maken => grafiek + animatie van de toestellen in de tijd
# - GUI koppelen aan simulatie
