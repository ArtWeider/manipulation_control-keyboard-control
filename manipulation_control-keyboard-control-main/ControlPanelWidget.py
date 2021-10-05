from tkinter import *
from tkinter import ttk
from config import Cfg as cfg


class ControlPanelWidget:

    mainLabel = None
    textLabel = None

    X = 1320 * cfg.SIZE_MULT
    Y = 345 * cfg.SIZE_MULT
    WIDTH = 275 * cfg.SIZE_MULT
    HEIGHT = 550 * cfg.SIZE_MULT

    def __init__(self):

        self.mainLabel = ttk.Frame(style="RoundedFrame", height=self.HEIGHT, width=self.WIDTH)
        self.mainLabel.place(x=self.X, y=self.Y)

        self.textLabel = Label(
            text="<ControlPanel>",
            font="Arial 14",
            height=1,
            bg=cfg.SUBCOLOR,
            fg=cfg.TEXT_COLOR,
        )
        #self.textLabel.place(x=self.X + 65, y=self.Y)



