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

    def getFG(self, str):
        f_limit = cfg.ManipulatorConfig.F_POINTS
        g_limit = cfg.ManipulatorConfig.G_POINTS
        f = f_limit[1]
        g = g_limit[1]
        try:
            splitted = str.split(r' ')
            if len(splitted) != 2: return f_limit[1], g_limit[1]
        except:
            return f_limit[1], g_limit[1]
        try:
            f = int(splitted[0])
        except: pass
        try:
            g = int(splitted[1])
        except: pass

        if f < f_limit[0]: f = f_limit[0]
        elif f > f_limit[2]: f = f_limit[2]
        else: f = f_limit[1]

        if g < g_limit[0]: g = g_limit[0]
        elif g > g_limit[2]: g = g_limit[2]
        else: g = g_limit[1]

        return f, g

    def setFG(self, f=None, g=None):
        cur_f, cur_g = self.getFG(self.fEntry.get())
        set_f, set_g = cur_f, cur_g

        if f != None: set_f = f
        if g != None: set_g = g

        self.fEntry.delete(0, END)
        self.fEntry.insert(0, f"{set_f} {set_g}")

    def isMouseOnWidget(self, event):
        return 925 < event.x < 1120 and -30 < event.y < 190

    def onEnterPressed(self, event):
        tag = self.main.timelineWidget.currentPoint[1]
        time = self.main.timelineWidget.tag2time[int(tag[1::])]
        save = self.main.savesManager.currentSave

        self.main.savesManager.saves[save].points[time].x = int(self.xEntry.get())
        self.main.graphicWidget.point.params['x'] = int(self.xEntry.get())

        self.main.savesManager.saves[save].points[time].y = int(self.yEntry.get())
        self.main.graphicWidget.point.params['y'] = int(self.yEntry.get())

        self.main.savesManager.saves[save].points[time].z = int(self.zEntry.get())
        self.main.graphicWidget.point.params['z'] = int(self.zEntry.get())

        self.main.savesManager.saves[save].points[time].q = int(self.qEntry.get())
        self.main.savesManager.saves[save].points[time].e = int(self.eEntry.get())

        f, g = self.getFG(self.fEntry.get())

        self.main.savesManager.saves[save].points[time].f = f
        self.main.savesManager.saves[save].points[time].g = g

        self.main.savesManager.saves[save].points[time].rad = int(self.radEntry.get())
        self.main.graphicWidget.point.params['rad'] = int(self.radEntry.get())

        self.main.savesManager.saves[save].points[time].a = int(self.aEntry.get())
        self.main.graphicWidget.point.params['a'] = int(self.aEntry.get())

        self.main.savesManager.saves[save].points[time].b = int(self.bEntry.get())
        self.main.graphicWidget.point.params['b'] = int(self.bEntry.get())

        self.main.savesManager.saves[save].points[time].c = int(self.cEntry.get())
        self.main.graphicWidget.point.params['c'] = int(self.cEntry.get())

        self.main.timelineWidget.movePoint(tag, int(self.timeEntry.get()) * self.main.timelineWidget.pixPerSecond)

        self.main.graphicWidget.point.getCoordinates()
        self.main.graphicWidget.point.getAngles()

        self.main.graphicWidget.point.assignPointCoords()

    def onPointToRobotPressed(self):
        controlPanel = self.main.controlPanelWidget
        self.clearAll(True, True)
        self.xEntry.insert(0, controlPanel.xEntry.get())
        self.yEntry.insert(0, controlPanel.yEntry.get())
        self.zEntry.insert(0, controlPanel.zEntry.get())
        self.qEntry.insert(0, int((controlPanel.qSlider.get() / 100) * cfg.ManipulatorConfig.Q_LIMIT[1]))
        self.eEntry.insert(0, int((controlPanel.eSlider.get() / 100) * cfg.ManipulatorConfig.E_LIMIT[1]))
        self.setFG(int((controlPanel.fSlider.get() / 100) * cfg.ManipulatorConfig.E_LIMIT[1]))
        self.radEntry.insert(0, str(0))
        self.aEntry.insert(0, str(0))
        self.bEntry.insert(0, str(0))
        self.cEntry.insert(0, str(0))

    def onRobotToPoint(self):
        self.main.controlPanelWidget.xEntry.delete(0, END)
        self.main.controlPanelWidget.yEntry.delete(0, END)
        self.main.controlPanelWidget.zEntry.delete(0, END)

        self.main.controlPanelWidget.xEntry.insert(0, self.xEntry.get())
        self.main.controlPanelWidget.yEntry.insert(0, self.yEntry.get())
        self.main.controlPanelWidget.zEntry.insert(0, self.zEntry.get())

        self.main.controlPanelWidget.qSlider.set((float(self.qEntry.get()) / cfg.ManipulatorConfig.Q_LIMIT[1]) * 100)
        self.main.controlPanelWidget.eSlider.set((float(self.eEntry.get()) / cfg.ManipulatorConfig.E_LIMIT[1]) * 100)
        self.main.controlPanelWidget.fSlider.set((float(self.getFG(self.fEntry.get())[0]) / cfg.ManipulatorConfig.F_LIMIT[1]) * 100)

        self.main.controlPanelWidget.qLabel.configure(text=f"Q: {self.qEntry.get()}")
        self.main.controlPanelWidget.eLabel.configure(text=f"E: {self.eEntry.get()}")
        self.main.controlPanelWidget.fLabel.configure(text=f"F: {self.getFG(self.fEntry.get())[0]}")

        self.main.controlPanelWidget.onEnterPressed(None)

    def onFollowCheckbuttonChanged(self):
        if self.followManipulatorVar.get():
            self.setStateAll(DISABLED, True)
        else:
            self.setStateAll(NORMAL, True)

    def onPointMoved(self, time):
        self.timeEntry.delete(0, END)
        self.timeEntry.insert(0, time)

    def onPointSelected(self, time):
        currentSave = self.main.savesManager.saves[self.main.savesManager.currentSave]
        point = currentSave.points[time]
        self.setStateAll(NORMAL)
        self.clearAll(True)
        self.xEntry.insert(0, point.x)
        self.yEntry.insert(0, point.y)
        self.zEntry.insert(0, point.z)
        self.qEntry.insert(0, point.q)
        self.eEntry.insert(0, point.e)
        self.setFG(point.f, point.g)
        self.radEntry.insert(0, point.rad)
        self.aEntry.insert(0, point.a)
        self.bEntry.insert(0, point.b)
        self.cEntry.insert(0, point.c)
        self.timeEntry.insert(0, point.time)

    def onPointDeselected(self):
        self.clearAll()
        self.setStateAll(DISABLED)

    def clearAll(self, ignoreCheckbutton=False, ignoreTime=False):
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
        if not ignoreTime:
            self.timeEntry.delete(0, END)
        if not ignoreCheckbutton:
            self.followManipulatorCheckbutton.deselect()

    def setStateAll(self, state, ignoreCheckbutton=False):
        self.xEntry.configure(state=state)
        self.yEntry.configure(state=state)
        self.zEntry.configure(state=state)
        self.radEntry.configure(state=state)
        self.aEntry.configure(state=state)
        self.bEntry.configure(state=state)
        self.cEntry.configure(state=state)
        self.timeEntry.configure(state=state)
        self.qEntry.configure(state=state)
        self.eEntry.configure(state=state)
        self.fEntry.configure(state=state)

        self.xLabel.configure(state=state)
        self.yLabel.configure(state=state)
        self.zLabel.configure(state=state)
        self.radLabel.configure(state=state)
        self.aLabel.configure(state=state)
        self.bLabel.configure(state=state)
        self.cLabel.configure(state=state)
        self.timeLabel.configure(state=state)
        self.qLabel.configure(state=state)
        self.eLabel.configure(state=state)
        self.fLabel.configure(state=state)

        if not ignoreCheckbutton:
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
                            state=DISABLED
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
                            fg=cfg.TEXT_COLOR,
                            state=DISABLED)
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
                            fg=cfg.TEXT_COLOR,
                            state=DISABLED)
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
                            fg=cfg.TEXT_COLOR,
                            state=DISABLED)
        self.radLabel.place(x=5, y=95)

        self.radEntry = Entry(width=3,
                            master=self.mainLabel,
                            font='Arial 11',
                            bg=cfg.SUBCOLOR,
                            bd=0,
                            fg=cfg.TEXT_COLOR,
                            justify=LEFT,
                            state=DISABLED,
                            disabledbackground=cfg.SUBCOLOR)
        self.radEntry.place(x=22, y=97)
        self.radEntry.bind('<Return>', self.onEnterPressed)

        self.aLabel = Label(master=self.mainLabel,
                            text="α: ",
                            font="Arial 11",
                            height=1,
                            bg=cfg.SUBCOLOR,
                            fg=cfg.TEXT_COLOR,
                            state=DISABLED)
        self.aLabel.place(x=50, y=95)

        self.aEntry = Entry(width=3,
                            master=self.mainLabel,
                            font='Arial 11',
                            bg=cfg.SUBCOLOR,
                            bd=0,
                            fg=cfg.TEXT_COLOR,
                            justify=LEFT,
                            state=DISABLED,
                            disabledbackground=cfg.SUBCOLOR)
        self.aEntry.place(x=65, y=97)
        self.aEntry.bind('<Return>', self.onEnterPressed)

        self.bLabel = Label(master=self.mainLabel,
                            text="β: ",
                            font="Arial 11",
                            height=1,
                            bg=cfg.SUBCOLOR,
                            fg=cfg.TEXT_COLOR,
                            state=DISABLED)
        self.bLabel.place(x=100, y=95)

        self.bEntry = Entry(width=3,
                            master=self.mainLabel,
                            font='Arial 11',
                            bg=cfg.SUBCOLOR,
                            bd=0,
                            fg=cfg.TEXT_COLOR,
                            justify=LEFT,
                            state=DISABLED,
                            disabledbackground=cfg.SUBCOLOR)
        self.bEntry.place(x=115, y=97)
        self.bEntry.bind('<Return>', self.onEnterPressed)

        self.cLabel = Label(master=self.mainLabel,
                             text="γ: ",
                             font="Arial 11",
                             height=1,
                             bg=cfg.SUBCOLOR,
                             fg=cfg.TEXT_COLOR,
                             state=DISABLED)
        self.cLabel.place(x=145, y=95)

        self.cEntry = Entry(width=3,
                             master=self.mainLabel,
                             font='Arial 11',
                             bg=cfg.SUBCOLOR,
                             bd=0,
                             fg=cfg.TEXT_COLOR,
                             justify=LEFT,
                             state=DISABLED,
                             disabledbackground=cfg.SUBCOLOR)
        self.cEntry.place(x=160, y=97)
        self.cEntry.bind('<Return>', self.onEnterPressed)

        self.qLabel = Label(master=self.mainLabel,
                            text="Q: ",
                            font="Arial 11",
                            height=1,
                            bg=cfg.SUBCOLOR,
                            fg=cfg.TEXT_COLOR,
                            state=DISABLED
                            )
        self.qLabel.place(x=5, y=67)

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
        self.qEntry.place(x=25, y=69)
        self.qEntry.bind('<Return>', self.onEnterPressed)

        self.eLabel = Label(master=self.mainLabel,
                            text="E: ",
                            font="Arial 11",
                            height=1,
                            bg=cfg.SUBCOLOR,
                            fg=cfg.TEXT_COLOR,
                            state=DISABLED)
        self.eLabel.place(x=70, y=67)

        self.eEntry = Entry(width=5,
                            master=self.mainLabel,
                            font='Arial 11',
                            bg=cfg.SUBCOLOR,
                            bd=0,
                            fg=cfg.TEXT_COLOR,
                            justify=LEFT,
                            state=DISABLED,
                            disabledbackground=cfg.SUBCOLOR)
        self.eEntry.place(x=90, y=69)
        self.eEntry.bind('<Return>', self.onEnterPressed)

        self.fLabel = Label(master=self.mainLabel,
                            text="F: ",
                            font="Arial 11",
                            height=1,
                            bg=cfg.SUBCOLOR,
                            fg=cfg.TEXT_COLOR,
                            state=DISABLED)
        self.fLabel.place(x=135, y=67)

        self.fEntry = Entry(width=5,
                            master=self.mainLabel,
                            font='Arial 11',
                            bg=cfg.SUBCOLOR,
                            bd=0,
                            fg=cfg.TEXT_COLOR,
                            justify=LEFT,
                            state=DISABLED,
                            disabledbackground=cfg.SUBCOLOR)
        self.fEntry.place(x=155, y=69)
        self.fEntry.bind('<Return>', self.onEnterPressed)

        self.timeLabel = Label(master=self.mainLabel,
                            text="Время: ",
                            font="Arial 11",
                            height=1,
                            bg=cfg.SUBCOLOR,
                            fg=cfg.TEXT_COLOR,
                            state=DISABLED)
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

        self.followManipulatorVar = BooleanVar()
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
                                                        onvalue=True,
                                                        offvalue=False,
                                                        variable=self.followManipulatorVar,
                                                        command=self.onFollowCheckbuttonChanged,
                                                        )
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
     
