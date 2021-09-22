from tkinter import *
from tkinter import ttk
from config import Cfg as cfg



class SavesWidget:

    mainFrame = None
    titleLabel = None
    whiteLineFrame = None
    listBox = None
    scrollBar = None

    X = 5 * cfg.SIZE_MULT
    Y = 30 * cfg.SIZE_MULT
    WIDTH = 200 * cfg.SIZE_MULT
    HEIGHT = 365 * cfg.SIZE_MULT

    def __init__(self):

        self.mainFrame = ttk.Frame(style="RoundedFrame", width=self.WIDTH, height=self.HEIGHT)
        self.mainFrame.place(x=self.X, y=self.Y)

        self.titleLabel = Label(
                               text="Сценарии",
                               font="Arial 11",
                               height=1,
                               bg=cfg.SUBCOLOR,
                               fg=cfg.TEXT_COLOR,
                               )
        self.titleLabel.place(x=self.X + 33, y=self.Y)

        self.whiteLineFrame = Frame(
                                    width=self.WIDTH-8,
                                    height=2,
                                    bg=cfg.LINE_COLOR)

        self.whiteLineFrame.place(x=self.X+4, y=self.Y+22)

        self.scrollBar = Scrollbar(master=self.mainFrame)

        self.listBox = Listbox(height=12,
                               width=16,
                               bd=0,
                               bg=cfg.SUBCOLOR,
                               highlightthickness=0,
                               selectbackground=cfg.MAIN_COLOR,
                               fg=cfg.TEXT_COLOR,
                               yscrollcommand=self.scrollBar.set,
                               selectmode=SINGLE,
                               font="Arial 11",
                               justify=CENTER
                               )
        self.listBox.place(x=self.X+7, y=self.Y+30)

        self.listBox.insert(0, "Сценарий 0", "Сценарий 1", "Сценарий 2", "Сценарий 3", "Сценарий 4", "Сценарий 5", "Сценарий 6", "Сценарий 7", "Сценарий 8", "Сценарий 9", )






