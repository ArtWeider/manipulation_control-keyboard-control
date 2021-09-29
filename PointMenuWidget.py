from tkinter import *
from tkinter import ttk
from config import Cfg as cfg

class PointMenuWidget:

    mainLabel = None
    textLabel = None

    X = 1320 * cfg.SIZE_MULT
    Y = 30 * cfg.SIZE_MULT
    WIDTH = 275 * cfg.SIZE_MULT
    HEIGHT = 310 * cfg.SIZE_MULT

    def __init__(self):

        self.mainLabel = ttk.Frame(style="RoundedFrame", height=self.HEIGHT, width=self.WIDTH)
        self.mainLabel.place(x=self.X, y=self.Y)

        self.textLabel = Label(
            master=self.mainLabel,
            text="Текущая точка",
            font="Arial 11",
            height=1,
            bg=cfg.SUBCOLOR,
            fg=cfg.TEXT_COLOR,
        )

        self.textLabel.place(x=43, y=4)

        self.whiteLineFrame = Frame(
            master=self.mainLabel,
            width=self.WIDTH - 8,
            height=2,
            bg=cfg.LINE_COLOR)

        self.whiteLineFrame.place(x=4, y=30)

        self.xLabel = Label(master=self.mainLabel,
                            text="X: ",
                            font="Arial 11",
                            height=1,
                            bg=cfg.SUBCOLOR,
                            fg=cfg.TEXT_COLOR)
        self.xLabel.place(x=15, y=37)

        self.xEntry = Entry(width=5,
                            master=self.mainLabel,
                            font='Arial 11',
                            bg=cfg.SUBCOLOR,
                            bd=0,
                            fg=cfg.TEXT_COLOR,
                            justify=LEFT,
                            state=DISABLED,
                            disabledbackground=cfg.SUBCOLOR)
        self.xEntry.place(x=35, y=39)

        self.yLabel = Label(master=self.mainLabel,
                            text="Y: ",
                            font="Arial 11",
                            height=1,
                            bg=cfg.SUBCOLOR,
                            fg=cfg.TEXT_COLOR)
        self.yLabel.place(x=70, y=37)

        self.yEntry = Entry(width=5,
                            master=self.mainLabel,
                            font='Arial 11',
                            bg=cfg.SUBCOLOR,
                            bd=0,
                            fg=cfg.TEXT_COLOR,
                            justify=LEFT,
                            state=DISABLED,
                            disabledbackground=cfg.SUBCOLOR)
        self.yEntry.place(x=90, y=39)

        self.zLabel = Label(master=self.mainLabel,
                            text="Z: ",
                            font="Arial 11",
                            height=1,
                            bg=cfg.SUBCOLOR,
                            fg=cfg.TEXT_COLOR)
        self.zLabel.place(x=125, y=37)

        self.zEntry = Entry(width=5,
                            master=self.mainLabel,
                            font='Arial 11',
                            bg=cfg.SUBCOLOR,
                            bd=0,
                            fg=cfg.TEXT_COLOR,
                            justify=LEFT,
                            state=DISABLED,
                            disabledbackground=cfg.SUBCOLOR)
        self.zEntry.place(x=145, y=39)

        self.qLabel = Label(master=self.mainLabel,
                            text="Q: ",
                            font="Arial 11",
                            height=1,
                            bg=cfg.SUBCOLOR,
                            fg=cfg.TEXT_COLOR)
        self.qLabel.place(x=15, y=67)

        self.qEntry = Entry(width=5,
                            master=self.mainLabel,
                            font='Arial 11',
                            bg=cfg.SUBCOLOR,
                            bd=0,
                            fg=cfg.TEXT_COLOR,
                            justify=LEFT,
                            state=DISABLED,
                            disabledbackground=cfg.SUBCOLOR)
        self.qEntry.place(x=35, y=69)

        self.q2Label = Label(master=self.mainLabel,
                            text="Q: ",
                            font="Arial 11",
                            height=1,
                            bg=cfg.SUBCOLOR,
                            fg=cfg.TEXT_COLOR)
        self.q2Label.place(x=70, y=67)

        self.q2Entry = Entry(width=5,
                            master=self.mainLabel,
                            font='Arial 11',
                            bg=cfg.SUBCOLOR,
                            bd=0,
                            fg=cfg.TEXT_COLOR,
                            justify=LEFT,
                            state=DISABLED,
                            disabledbackground=cfg.SUBCOLOR)
        self.q2Entry.place(x=90, y=69)

        self.q3Label = Label(master=self.mainLabel,
                             text="Q: ",
                             font="Arial 11",
                             height=1,
                             bg=cfg.SUBCOLOR,
                             fg=cfg.TEXT_COLOR)
        self.q3Label.place(x=125, y=67)

        self.q3Entry = Entry(width=5,
                             master=self.mainLabel,
                             font='Arial 11',
                             bg=cfg.SUBCOLOR,
                             bd=0,
                             fg=cfg.TEXT_COLOR,
                             justify=LEFT,
                             state=DISABLED,
                             disabledbackground=cfg.SUBCOLOR)
        self.q3Entry.place(x=145, y=69)

        self.timeLabel = Label(master=self.mainLabel,
                            text="Время: ",
                            font="Arial 11",
                            height=1,
                            bg=cfg.SUBCOLOR,
                            fg=cfg.TEXT_COLOR)
        self.timeLabel.place(x=15, y=97)

        self.timeEntry = Entry(width=5,
                            master=self.mainLabel,
                            font='Arial 11',
                            bg=cfg.SUBCOLOR,
                            bd=0,
                            fg=cfg.TEXT_COLOR,
                            justify=LEFT,
                            state=DISABLED,
                            disabledbackground=cfg.SUBCOLOR)
        self.timeEntry.place(x=70, y=100)

        self.followManipulatorCheckbutton = Checkbutton(master=self.mainLabel,
                                                           text='Следовать',
                                                           bg=cfg.SUBCOLOR,
                                                           activebackground=cfg.SUBCOLOR,
                                                           activeforeground=cfg.TEXT_COLOR,
                                                           borderwidth=0,
                                                           relief=FLAT,
                                                           selectcolor=cfg.MAIN_COLOR,
                                                           fg=cfg.TEXT_COLOR,
                                                           font='Arial 11',
                                                           state=DISABLED,
                                                           disabledforeground=cfg.TEXT_COLOR)
        self.followManipulatorCheckbutton.place(x=15, y=125)

        self.pointToRobotButton = Button(master=self.mainLabel,
                                   text="Точку к манипулятору",
                                   bg=cfg.BUTTON_COLOR,
                                   bd=0,
                                   fg=cfg.TEXT_COLOR,
                                   width=23,
                                   activebackground=cfg.BUTTON_ACTIVE_COLOR,
                                   activeforeground=cfg.TEXT_COLOR,
                                   state=DISABLED,
                                   )
        self.pointToRobotButton.place(x=15, y=155)

        self.robotToPointButton = Button(master=self.mainLabel,
                                         text="Манипулятор к точке",
                                         bg=cfg.BUTTON_COLOR,
                                         bd=0,
                                         fg=cfg.TEXT_COLOR,
                                         width=23,
                                         activebackground=cfg.BUTTON_ACTIVE_COLOR,
                                         activeforeground=cfg.TEXT_COLOR,
                                         state=DISABLED,
                                         )
        self.robotToPointButton.place(x=15, y=185)






