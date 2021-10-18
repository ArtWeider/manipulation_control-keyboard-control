from tkinter import *
from tkinter import ttk
from config import Cfg as cfg

class PointMenuWidget:

    mainLabel = None
    textLabel = None

    X = 1320 * cfg.SIZE_MULT
    Y = 30 * cfg.SIZE_MULT
    WIDTH = 275 * cfg.SIZE_MULT
    HEIGHT = 350 * cfg.SIZE_MULT

    def isMouseOnWidget(self, event):
        return 925 < event.x < 1120 and -30 < event.y < 190

    def onEnterPressed(self, event):
        tag = self.main.timelineWidget.currentPoint[1]
        time = self.main.timelineWidget.tag2time[int(tag[1::])]
        save = self.main.savesManager.currentSave

        if str(event.widget) == ".!frame3.!entry":
            self.main.savesManager.saves[save].points[time].x = float(self.xEntry.get())
            self.main.graphicWidget.point.params['x'] = float(self.xEntry.get())
            self.main.graphicWidget.point.getAngles()

        elif str(event.widget) == ".!frame3.!entry2":
            self.main.savesManager.saves[save].points[time].y = float(self.yEntry.get())
            self.main.graphicWidget.point.params['y'] = float(self.yEntry.get())
            self.main.graphicWidget.point.getAngles()

        elif str(event.widget) == ".!frame3.!entry3":
            self.main.savesManager.saves[save].points[time].z = float(self.zEntry.get())
            self.main.graphicWidget.point.params['z'] = float(self.zEntry.get())
            self.main.graphicWidget.point.getAngles()

        elif str(event.widget) == ".!frame3.!entry4":
            self.main.savesManager.saves[save].points[time].rad = float(self.radEntry.get())
            self.main.graphicWidget.point.params['rad'] = float(self.radEntry.get())
            self.main.graphicWidget.point.getCoordinates()

        elif str(event.widget) == ".!frame3.!entry5":
            self.main.savesManager.saves[save].points[time].a = float(self.aEntry.get())
            self.main.graphicWidget.point.params['a'] = float(self.aEntry.get())
            self.main.graphicWidget.point.getCoordinates()

        elif str(event.widget) == ".!frame3.!entry6":
            self.main.savesManager.saves[save].points[time].b = float(self.bEntry.get())
            self.main.graphicWidget.point.params['b'] = float(self.bEntry.get())
            self.main.graphicWidget.point.getCoordinates()

        elif str(event.widget) == ".!frame3.!entry7":
            self.main.savesManager.saves[save].points[time].c = float(self.cEntry.get())
            self.main.graphicWidget.point.params['c'] = float(self.cEntry.get())
            self.main.graphicWidget.point.getCoordinates()

        elif str(event.widget) == ".!frame3.!entry11":
            self.main.timelineWidget.movePoint(tag, float(self.timeEntry.get()) * self.main.timelineWidget.pixPerSecond)

        self.main.graphicWidget.point.assignPointCoords()
        self.onPointSelected(self.main.graphicWidget.point.selectedTime)

    def onPointToRobotPressed(self):
        controlPanel = self.main.controlPanelWidget
        self.clearAll()
        self.xEntry.insert(0, controlPanel.xEntry.get())
        self.yEntry.insert(0, controlPanel.yEntry.get())
        self.zEntry.insert(0, controlPanel.zEntry.get())
        self.qEntry.insert(0, (controlPanel.qSlider.get() / 100) * cfg.ManipulatorConfig.Q_LIMIT[1])
        self.eEntry.insert(0, controlPanel.eSlider.get())
        self.fEntry.insert(0, controlPanel.fSlider.get())

    def onRobotToPoint(self):
        self.main.controlPanelWidget.xEntry.delete(0, END)
        self.main.controlPanelWidget.yEntry.delete(0, END)
        self.main.controlPanelWidget.zEntry.delete(0, END)
        self.main.controlPanelWidget.xEntry.insert(0, self.xEntry.get())
        self.main.controlPanelWidget.yEntry.insert(0, self.yEntry.get())
        self.main.controlPanelWidget.zEntry.insert(0, self.zEntry.get())
        self.main.controlPanelWidget.qSlider.set((float(self.qEntry.get()) / cfg.ManipulatorConfig.Q_LIMIT[1]) * 100)
        self.main.controlPanelWidget.onEnterPressed(None)

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
        self.radEntry.insert(0, point.rad)
        self.aEntry.insert(0, point.a)
        self.bEntry.insert(0, point.b)
        self.cEntry.insert(0, point.c)
        self.qEntry.insert(0, point.a)
        self.eEntry.insert(0, point.b)
        self.fEntry.insert(0, point.c)
        self.timeEntry.insert(0, point.time)

    def onPointDeselected(self):
        self.clearAll()
        self.setStateAll(DISABLED)

    def clearAll(self):
        self.xEntry.delete(0, END)
        self.yEntry.delete(0, END)
        self.zEntry.delete(0, END)
        self.radEntry.delete(0, END)
        self.aEntry.delete(0, END)
        self.bEntry.delete(0, END)
        self.cEntry.delete(0, END)
        self.qEntry.delete(0, END)
        self.eEntry.delete(0, END)
        self.fEntry.delete(0, END)
        self.timeEntry.delete(0, END)
        self.followManipulatorCheckbutton.deselect()

    def setStateAll(self, state):
        self.xEntry.configure(state=state)
        self.yEntry.configure(state=state)
        self.zEntry.configure(state=state)
        self.radEntry.configure(state=state)
        self.aEntry.configure(state=state)
        self.bEntry.configure(state=state)
        self.cEntry.configure(state=state)
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

        self.radLabel = Label(master=self.mainLabel,
                            text="R: ",
                            font="Arial 11",
                            height=1,
                            bg=cfg.SUBCOLOR,
                            fg=cfg.TEXT_COLOR)
        self.radLabel.place(x=5, y=67)

        self.radEntry = Entry(width=3,
                            master=self.mainLabel,
                            font='Arial 11',
                            bg=cfg.SUBCOLOR,
                            bd=0,
                            fg=cfg.TEXT_COLOR,
                            justify=LEFT,
                            state=DISABLED,
                            disabledbackground=cfg.SUBCOLOR)
        self.radEntry.place(x=22, y=69)
        self.radEntry.bind('<Return>', self.onEnterPressed)

        self.aLabel = Label(master=self.mainLabel,
                            text="α: ",
                            font="Arial 11",
                            height=1,
                            bg=cfg.SUBCOLOR,
                            fg=cfg.TEXT_COLOR)
        self.aLabel.place(x=50, y=67)

        self.aEntry = Entry(width=3,
                            master=self.mainLabel,
                            font='Arial 11',
                            bg=cfg.SUBCOLOR,
                            bd=0,
                            fg=cfg.TEXT_COLOR,
                            justify=LEFT,
                            state=DISABLED,
                            disabledbackground=cfg.SUBCOLOR)
        self.aEntry.place(x=65, y=69)
        self.aEntry.bind('<Return>', self.onEnterPressed)

        self.bLabel = Label(master=self.mainLabel,
                            text="β: ",
                            font="Arial 11",
                            height=1,
                            bg=cfg.SUBCOLOR,
                            fg=cfg.TEXT_COLOR)
        self.bLabel.place(x=100, y=67)

        self.bEntry = Entry(width=3,
                            master=self.mainLabel,
                            font='Arial 11',
                            bg=cfg.SUBCOLOR,
                            bd=0,
                            fg=cfg.TEXT_COLOR,
                            justify=LEFT,
                            state=DISABLED,
                            disabledbackground=cfg.SUBCOLOR)
        self.bEntry.place(x=115, y=69)
        self.bEntry.bind('<Return>', self.onEnterPressed)

        self.cLabel = Label(master=self.mainLabel,
                             text="γ: ",
                             font="Arial 11",
                             height=1,
                             bg=cfg.SUBCOLOR,
                             fg=cfg.TEXT_COLOR)
        self.cLabel.place(x=145, y=67)

        self.cEntry = Entry(width=3,
                             master=self.mainLabel,
                             font='Arial 11',
                             bg=cfg.SUBCOLOR,
                             bd=0,
                             fg=cfg.TEXT_COLOR,
                             justify=LEFT,
                             state=DISABLED,
                             disabledbackground=cfg.SUBCOLOR)
        self.cEntry.place(x=160, y=69)
        self.cEntry.bind('<Return>', self.onEnterPressed)

        self.qLabel = Label(master=self.mainLabel,
                            text="Q: ",
                            font="Arial 11",
                            height=1,
                            bg=cfg.SUBCOLOR,
                            fg=cfg.TEXT_COLOR,
                            )
        self.qLabel.place(x=5, y=95)

        self.qEntry = Entry(width=5,
                            master=self.mainLabel,
                            font='Arial 11',
                            bg=cfg.SUBCOLOR,
                            bd=0,
                            fg=cfg.TEXT_COLOR,
                            justify=LEFT,
                            state=DISABLED,
                            disabledbackground=cfg.SUBCOLOR,
                            )
        self.qEntry.place(x=25, y=97)
        self.qEntry.bind('<Return>', self.onEnterPressed)

        self.eLabel = Label(master=self.mainLabel,
                            text="E: ",
                            font="Arial 11",
                            height=1,
                            bg=cfg.SUBCOLOR,
                            fg=cfg.TEXT_COLOR)
        self.eLabel.place(x=70, y=95)

        self.eEntry = Entry(width=5,
                            master=self.mainLabel,
                            font='Arial 11',
                            bg=cfg.SUBCOLOR,
                            bd=0,
                            fg=cfg.TEXT_COLOR,
                            justify=LEFT,
                            state=DISABLED,
                            disabledbackground=cfg.SUBCOLOR)
        self.eEntry.place(x=90, y=97)
        self.eEntry.bind('<Return>', self.onEnterPressed)

        self.fLabel = Label(master=self.mainLabel,
                            text="F: ",
                            font="Arial 11",
                            height=1,
                            bg=cfg.SUBCOLOR,
                            fg=cfg.TEXT_COLOR)
        self.fLabel.place(x=135, y=95)

        self.fEntry = Entry(width=5,
                            master=self.mainLabel,
                            font='Arial 11',
                            bg=cfg.SUBCOLOR,
                            bd=0,
                            fg=cfg.TEXT_COLOR,
                            justify=LEFT,
                            state=DISABLED,
                            disabledbackground=cfg.SUBCOLOR)
        self.fEntry.place(x=155, y=97)
        self.fEntry.bind('<Return>', self.onEnterPressed)

        self.timeLabel = Label(master=self.mainLabel,
                            text="Время: ",
                            font="Arial 11",
                            height=1,
                            bg=cfg.SUBCOLOR,
                            fg=cfg.TEXT_COLOR)
        self.timeLabel.place(x=5, y=127)

        self.timeEntry = Entry(width=5,
                            master=self.mainLabel,
                            font='Arial 11',
                            bg=cfg.SUBCOLOR,
                            bd=0,
                            fg=cfg.TEXT_COLOR,
                            justify=LEFT,
                            state=DISABLED,
                            disabledbackground=cfg.SUBCOLOR)
        self.timeEntry.place(x=60, y=130)
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
        self.followManipulatorCheckbutton.place(x=5, y=155)

        self.pointToRobotButton = Button(master=self.mainLabel,
                                   text="Точку к манипулятору",
                                   bg=cfg.BUTTON_COLOR,
                                   bd=0,
                                   fg=cfg.TEXT_COLOR,
                                   width=23,
                                   activebackground=cfg.BUTTON_ACTIVE_COLOR,
                                   activeforeground=cfg.TEXT_COLOR,
                                   state=DISABLED,
                                   command=self.onPointToRobotPressed
                                   )
        self.pointToRobotButton.place(x=15, y=185)

        self.robotToPointButton = Button(master=self.mainLabel,
                                         text="Манипулятор к точке",
                                         bg=cfg.BUTTON_COLOR,
                                         bd=0,
                                         fg=cfg.TEXT_COLOR,
                                         width=23,
                                         activebackground=cfg.BUTTON_ACTIVE_COLOR,
                                         activeforeground=cfg.TEXT_COLOR,
                                         state=DISABLED,
                                         command=self.onRobotToPoint
                                         )
        self.robotToPointButton.place(x=15, y=215)
     
