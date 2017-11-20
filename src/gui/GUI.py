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

# Make image of the house
drawing_house = PhotoImage(file="drawing_house.png")
drawing_house_width = drawing_house.width()
drawing_house_height = drawing_house.height()
house = Label(root, image=drawing_house, background="white")
house.place(x=screen_width/2-drawing_house_width/2, y=screen_height/2-drawing_house_height/2)

# make image of the logo
drawing_logo = PhotoImage(file="logo.png")
drawing_logo_width = drawing_logo.width()
drawing_logo_height = drawing_logo.height()
logo = Label(root, image=drawing_logo, borderwidth=0)
logo.place(x=screen_width-drawing_logo_width-10, y=10)

# make the optionmenu's to chose your input
variable_sun_panel = StringVar(root)
variable_sun_panel.set("maak u keuze")
sun_panel_menu = OptionMenu(root, variable_sun_panel, "wel zonnepanelen", "geen zonnepanelen", command=slider_sun_panel)
sun_panel_menu.configure(width=30, relief=SOLID, background="white", activebackground="white",
                         highlightbackground="white")
sun_panel_menu.place(x=10, y=50)

variable_wind_turbine_and_battery = StringVar(root)
variable_wind_turbine_and_battery.set("maak u keuze")
wind_turbine_and_battery_menu = OptionMenu(root, variable_wind_turbine_and_battery, "wel windmolen en thuisbatterij",
                                           "geen windmolen en thuisbatterij")
wind_turbine_and_battery_menu.configure(width=30, relief=SOLID, background="white", activebackground="white",
                                        highlightbackground="white")
wind_turbine_and_battery_menu.place(x=240, y=50)

variable_electric_car = StringVar(root)
variable_electric_car.set("maak u keuze")
electric_car_menu = OptionMenu(root, variable_electric_car, "elektrische wagen", "brandstof wagen",
                               command=slider_electric_car)
electric_car_menu.configure(width=30, relief=SOLID, background="white", activebackground="white",
                            highlightbackground="white")
electric_car_menu.place(x=470, y=50)

variable_house = StringVar(root)
variable_house.set("maak u keuze")
house_menu = OptionMenu(root, variable_house, "nieuwbouw", "bestaand huis")
house_menu.configure(width=30, relief=SOLID, background="white", activebackground="white", highlightbackground="white")
house_menu.place(x=700, y=50)

# Make sliders to select number of sun panels and cars
nb_sun_panel = Scale(root, from_=1, to=10, orient=HORIZONTAL, background="white", borderwidth=1,
                     sliderrelief=FLAT, troughcolor="black", highlightbackground="white")

nb_electric_car = Scale(root, from_=1, to=10, orient=HORIZONTAL, background="white", borderwidth=1, sliderrelief=FLAT,
                        troughcolor="black", highlightbackground="white")

# Create a button to start the simulation
button = Button(root, text='Start simulatie', width=25, height=5, relief=SOLID, background="white",
                activebackground="white")
button.place(x=screen_width/2-90, y=screen_height-100)


root.mainloop()

# TODO:
# - al dan niet tonen van de geselecteerde input in de tekening
# - outputscreen maken => grafiek + animatie van de toestellen in de tijd
# - GUI koppelen aan simulatie
