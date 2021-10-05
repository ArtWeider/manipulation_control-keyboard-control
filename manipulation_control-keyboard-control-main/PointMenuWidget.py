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

    def isMouseOnWidget(self, event):
        return 925 < event.x < 1120 and -30 < event.y < 190

    def onEnterPressed(self, event):
        tag = self.main.timelineWidget.currentPoint[1]
        time = self.main.timelineWidget.tag2time[int(tag[1::])]
        save = self.main.savesManager.currentSave

        self.main.savesManager.saves[save].points[time].x = float(self.xEntry.get())
        self.main.savesManager.saves[save].points[time].y = float(self.yEntry.get())
        self.main.savesManager.saves[save].points[time].z = float(self.zEntry.get())
        
        self.main.graphicWidget.point.params['x'] = float(self.xEntry.get())
        self.main.graphicWidget.point.params['y'] = float(self.yEntry.get())
        self.main.graphicWidget.point.params['z'] = float(self.zEntry.get())

        self.main.timelineWidget.movePoint(tag, float(self.timeEntry.get()) * self.main.timelineWidget.pixPerSecond)


    def onPointMoved(self, time):
        self.timeEntry.delete(0, END)
        self.timeEntry.insert(0, time)

    def onPointSelected(self, time):
        currentSave = self.main.savesManager.saves[self.main.savesManager.currentSave]
        point = currentSave.points[time]
        self.setStateAll(NORMAL)
        self.clearAll()
        self.xEntry.insert(0, point.x)
        self.yEntry.insert(0, point.y)
        self.zEntry.insert(0, point.z)
        self.qEntry.insert(0, "000")
        self.q2Entry.insert(0, "000")
        self.q3Entry.insert(0, "000")
        self.timeEntry.insert(0, point.time)

    def onPointDeselected(self):
        self.clearAll()
        self.setStateAll(DISABLED)

    def clearAll(self):
        self.xEntry.delete(0, END)
        self.yEntry.delete(0, END)
        self.zEntry.delete(0, END)
        self.qEntry.delete(0, END)
        self.q2Entry.delete(0, END)
        self.q3Entry.delete(0, END)
        self.timeEntry.delete(0, END)
        self.followManipulatorCheckbutton.deselect()

    def setStateAll(self, state):
        self.xEntry.configure(state=state)
        self.yEntry.configure(state=state)
        self.zEntry.configure(state=state)
        self.qEntry.configure(state=state)
        self.q2Entry.configure(state=state)
        self.q3Entry.configure(state=state)
        self.timeEntry.configure(state=state)
        self.followManipulatorCheckbutton.configure(state=state)
        self.robotToPointButton.configure(state=state)
        self.pointToRobotButton.configure(state=state)

    def __init__(self, main):

        self.main = main

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
                            fg=cfg.TEXT_COLOR,
                            )
        self.xLabel.place(x=5, y=37)

        self.xEntry = Entry(width=5,
                            master=self.mainLabel,
                            font='Arial 11',
                            bg=cfg.SUBCOLOR,
                            bd=0,
                            fg=cfg.TEXT_COLOR,
                            justify=LEFT,
                            state=DISABLED,
                            disabledbackground=cfg.SUBCOLOR,
                            )
        self.xEntry.place(x=25, y=39)
        self.xEntry.bind('<Return>', self.onEnterPressed)

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
        self.yEntry.bind('<Return>', self.onEnterPressed)

        self.zLabel = Label(master=self.mainLabel,
                            text="Z: ",
                            font="Arial 11",
                            height=1,
                            bg=cfg.SUBCOLOR,
                            fg=cfg.TEXT_COLOR)
        self.zLabel.place(x=135, y=37)

        self.zEntry = Entry(width=5,
                            master=self.mainLabel,
                            font='Arial 11',
                            bg=cfg.SUBCOLOR,
                            bd=0,
                            fg=cfg.TEXT_COLOR,
                            justify=LEFT,
                            state=DISABLED,
                            disabledbackground=cfg.SUBCOLOR)
        self.zEntry.place(x=155, y=39)
        self.zEntry.bind('<Return>', self.onEnterPressed)

        self.qLabel = Label(master=self.mainLabel,
                            text="Q: ",
                            font="Arial 11",
                            height=1,
                            bg=cfg.SUBCOLOR,
                            fg=cfg.TEXT_COLOR)
        self.qLabel.place(x=5, y=67)

        self.qEntry = Entry(width=5,
                            master=self.mainLabel,
                            font='Arial 11',
                            bg=cfg.SUBCOLOR,
                            bd=0,
                            fg=cfg.TEXT_COLOR,
                            justify=LEFT,
                            state=DISABLED,
                            disabledbackground=cfg.SUBCOLOR)
        self.qEntry.place(x=25, y=69)
        self.qEntry.bind('<Return>', self.onEnterPressed)

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
        self.q2Entry.bind('<Return>', self.onEnterPressed)

        self.q3Label = Label(master=self.mainLabel,
                             text="Q: ",
                             font="Arial 11",
                             height=1,
                             bg=cfg.SUBCOLOR,
                             fg=cfg.TEXT_COLOR)
        self.q3Label.place(x=135, y=67)

        self.q3Entry = Entry(width=5,
                             master=self.mainLabel,
                             font='Arial 11',
                             bg=cfg.SUBCOLOR,
                             bd=0,
                             fg=cfg.TEXT_COLOR,
                             justify=LEFT,
                             state=DISABLED,
                             disabledbackground=cfg.SUBCOLOR)
        self.q3Entry.place(x=155, y=69)
        self.q3Entry.bind('<Return>', self.onEnterPressed)

        self.timeLabel = Label(master=self.mainLabel,
                            text="Время: ",
                            font="Arial 11",
                            height=1,
                            bg=cfg.SUBCOLOR,
                            fg=cfg.TEXT_COLOR)
        self.timeLabel.place(x=5, y=97)

        self.timeEntry = Entry(width=5,
                            master=self.mainLabel,
                            font='Arial 11',
                            bg=cfg.SUBCOLOR,
                            bd=0,
                            fg=cfg.TEXT_COLOR,
                            justify=LEFT,
                            state=DISABLED,
                            disabledbackground=cfg.SUBCOLOR)
        self.timeEntry.place(x=60, y=100)
        self.timeEntry.bind('<Return>', self.onEnterPressed)

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
        self.followManipulatorCheckbutton.place(x=5, y=125)

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






