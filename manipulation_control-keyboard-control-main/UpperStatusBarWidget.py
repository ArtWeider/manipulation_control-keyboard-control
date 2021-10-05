from tkinter import *
from config import Cfg as cfg

class UpperStatusBar:

    mainLabel = None
    label = None
    bottomLine = None

    def __init__(self):

        self.mainLabel = Label(border=0, bg=cfg.MAIN_COLOR, height=1, text="<Status>",
                           anchor="center",
                           padx=20,
                           pady=2,
                           font="Arial 11", fg=cfg.TEXT_COLOR,)
        self.mainLabel.pack(side=TOP, fill=BOTH)





