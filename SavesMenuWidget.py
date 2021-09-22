from tkinter import *
from tkinter import ttk
from config import Cfg as cfg
from PIL import Image, ImageTk


class SavesMenuWidget:

    mainFrame = None
    createButton = None
    nameEntry = None

    X = 5 * cfg.SIZE_MULT
    Y = 400 * cfg.SIZE_MULT
    WIDTH = 200 * cfg.SIZE_MULT
    HEIGHT = 195 * cfg.SIZE_MULT

    def __init__(self):

        self.mainFrame = ttk.Frame(style="RoundedFrame", height=self.HEIGHT, width=self.WIDTH)
        self.mainFrame.place(x=self.X, y=self.Y)

        self.nameEntry = Entry(master=self.mainFrame,
                               width=19,
                               bg=cfg.MAIN_COLOR,
                               bd=0,
                               fg=cfg.TEXT_COLOR,
                               justify=CENTER
                               )
        self.nameEntry.place(x=13, y=10)

        self.createButton = Button(master=self.mainFrame,
                                   text="Создать",
                                   bg=cfg.BUTTON_COLOR,
                                   bd=0,
                                   fg=cfg.TEXT_COLOR,
                                   width=16,
                                   activebackground=cfg.BUTTON_ACTIVE_COLOR,
                                   activeforeground=cfg.TEXT_COLOR
                                   )
        self.createButton.place(x=12, y=35)

        self.deleteButton = Button(master=self.mainFrame,
                                   text="Удалить",
                                   bg=cfg.BUTTON_COLOR,
                                   bd=0,
                                   fg=cfg.TEXT_COLOR,
                                   width=16,
                                   activebackground=cfg.BUTTON_ACTIVE_COLOR,
                                   activeforeground=cfg.TEXT_COLOR
                                   )
        self.deleteButton.place(x=12, y=65)

        self.saveButton = Button(master=self.mainFrame,
                                 text="Сохранить",
                                 bg=cfg.BUTTON_COLOR,
                                 bd=0,
                                 fg=cfg.TEXT_COLOR,
                                 width=16,
                                 activebackground=cfg.BUTTON_ACTIVE_COLOR,
                                 activeforeground=cfg.TEXT_COLOR
                                   )
        self.saveButton.place(x=12, y=95)








