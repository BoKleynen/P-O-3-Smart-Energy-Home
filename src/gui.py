import tkinter as tk
from typing import Dict, Any


LARGE_FONT = ("Verdana", 12)


class SmartEnergyHomeApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frame_dict: Dict[Any, tk.Frame] = {}

        frame = StartPage(container, self)
        self.frame_dict[StartPage] = frame
        frame.grid(row=0,column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        self.frame_dict.get(cont).tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, cont):
        super().__init__(parent)
        label = tk.Label(self, text="start page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="visit page 1")
        button1.pack()


app = SmartEnergyHomeApp()
app.mainloop()