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

    validation = False

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

        self.main.savesManager.saves[save].points[time].f = int(self.fEntry.get())
        self.main.savesManager.saves[save].points[time].gMode = bool(self.changeFGVar.get())

        self.main.timelineWidget.movePoint(tag, float(self.timeEntry.get()) * self.main.timelineWidget.pixPerSecond)

        self.main.graphicWidget.point.getCoordinates()
        self.main.graphicWidget.point.getAngles()

        self.main.graphicWidget.point.assignPointCoords()
        self.main.savesManager.save(self.main.savesManager.saves[self.main.savesManager.currentSave])

    def validate(self, action, value, entry):
        return True

    def onPointToRobotPressed(self):
        controlPanel = self.main.controlPanelWidget
        self.clearAll(True, True)
        self.xEntry.insert(0, controlPanel.xEntry.get())
        self.yEntry.insert(0, controlPanel.yEntry.get())
        self.zEntry.insert(0, controlPanel.zEntry.get())
        self.qEntry.insert(0, int(float(self.main.controlPanelWidget.qLabel.cget('text')[2::])))
        self.eEntry.insert(0, int(float(self.main.controlPanelWidget.eLabel.cget('text')[2::])))
        self.fEntry.insert(0, int(float(self.main.controlPanelWidget.fLabel.cget('text')[2::])))
        self.setFGMode(self.main.manipulatorController.gMode, True)
        self.onEnterPressed(None)

    def onRobotToPoint(self):
        self.main.controlPanelWidget.xEntry.delete(0, END)
        self.main.controlPanelWidget.yEntry.delete(0, END)
        self.main.controlPanelWidget.zEntry.delete(0, END)

        self.main.controlPanelWidget.xEntry.insert(0, self.xEntry.get())
        self.main.controlPanelWidget.yEntry.insert(0, self.yEntry.get())
        self.main.controlPanelWidget.zEntry.insert(0, self.zEntry.get())

        self.main.controlPanelWidget.qSlider.set((float(self.qEntry.get()) / cfg.ManipulatorConfig.Q_LIMIT[1]) * 100)
        self.main.controlPanelWidget.eSlider.set((float(self.eEntry.get()) / cfg.ManipulatorConfig.E_LIMIT[1]) * 100)
        self.main.controlPanelWidget.fSlider.set((float(self.fEntry.get()) / cfg.ManipulatorConfig.F_LIMIT[1]) * 100)

        self.main.manipulatorController.gMode = bool(self.changeFGVar.get())

        self.main.controlPanelWidget.qLabel.configure(text=f"Q: {self.qEntry.get()}")
        self.main.controlPanelWidget.eLabel.configure(text=f"E: {self.eEntry.get()}")
        self.main.controlPanelWidget.fLabel.configure(text=f"F: {self.fEntry.get()}")

        self.main.manipulatorController.goToPoint(x=float(self.xEntry.get()),
                                                  y=float(self.yEntry.get()),
                                                  z=float(self.zEntry.get()),
                                                  q=int(self.qEntry.get()),
                                                  e=int(self.eEntry.get()),
                                                  f=int(self.fEntry.get()),
                                                  gMode=bool(self.changeFGVar.get()))

    def onFollowCheckbuttonChanged(self):
        if self.followManipulatorVar.get():
            self.setStateAll(DISABLED, True)

        else:
            self.setStateAll(NORMAL, True)

    def onPointMoved(self, time):
        self.timeEntry.delete(0, END)
        self.timeEntry.insert(0, time)

    def onPointSelected(self, time):
        self.validation = False
        currentSave = self.main.savesManager.saves[self.main.savesManager.currentSave]
        point = currentSave.points[time]
        self.setStateAll(NORMAL)
        self.clearAll(True)
        self.xEntry.insert(0, point.x)
        self.yEntry.insert(0, point.y)
        self.zEntry.insert(0, point.z)
        self.qEntry.insert(0, point.q)
        self.eEntry.insert(0, point.e)
        self.fEntry.insert(0, point.f)
        self.setFGMode(point.gMode, True)
        self.timeEntry.insert(0, point.time)
        self.validation = True

    def onPointDeselected(self):
        self.validation = False
        self.followManipulatorVar.set(0)
        self.followManipulatorCheckbutton.deselect()
        self.clearAll()
        self.setStateAll(DISABLED)

    def setFGMode(self, gMode, setButtons):
        if gMode:
            self.fLabel.configure(text='G:')
        else:
            self.fLabel.configure(text='F:')

        self.main.savesManager.saves[self.main.savesManager.currentSave].points[
            self.main.timelineWidget.tag2time[int(self.main.timelineWidget.currentPoint[1][1::])]].gMode = gMode

        if setButtons:
            self.changeFGVar.set(int(gMode))

    def onRadiobuttonChanged(self):
        self.setFGMode(bool(self.changeFGVar.get()), False)

    def clearAll(self, ignoreCheckbutton=False, ignoreTime=False):
        self.xEntry.delete(0, END)
        self.yEntry.delete(0, END)
        self.zEntry.delete(0, END)
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
        self.timeEntry.configure(state=state)
        self.qEntry.configure(state=state)
        self.eEntry.configure(state=state)
        self.fEntry.configure(state=state)
        self.fRadiobutton.configure(state=state)
        self.gRadiobutton.configure(state=state)

        self.xLabel.configure(state=state)
        self.yLabel.configure(state=state)
        self.zLabel.configure(state=state)
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

        self.validateCommand = self.mainLabel.register(self.validate)

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
                            validate='key',
                            validatecommand=(self.validateCommand, '%d', '%P', '%W')
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
                            disabledbackground=cfg.SUBCOLOR,
                            validate='key',
                            validatecommand=(self.validateCommand, '%d', '%P', '%W')
                            )
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
                            disabledbackground=cfg.SUBCOLOR,
                            validate='key',
                            validatecommand=(self.validateCommand, '%d', '%P', '%W')
                            )
        self.zEntry.place(x=155, y=39)
        self.zEntry.bind('<Return>', self.onEnterPressed)

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
                            validate='key',
                            validatecommand=(self.validateCommand, '%d', '%P', '%W')
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
                            disabledbackground=cfg.SUBCOLOR,
                            validate='key',
                            validatecommand=(self.validateCommand, '%d', '%P', '%W')
                            )
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
                            disabledbackground=cfg.SUBCOLOR,
                            validate='key',
                            validatecommand=(self.validateCommand, '%d', '%P', '%W')
                            )
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
                            disabledbackground=cfg.SUBCOLOR,
                               validate='key',
                               validatecommand=(self.validateCommand, '%d', '%P', '%W')
                               )
        self.timeEntry.place(x=60, y=130)
        self.timeEntry.bind('<Return>', self.onEnterPressed)

        self.changeFGVar = IntVar()
        self.fRadiobutton = Radiobutton(master=self.mainLabel,
                                        text='F',
                                        variable=self.changeFGVar,
                                        value=0,
                                        font='Arial 11',
                                        bg=cfg.SUBCOLOR,
                                        bd=0,
                                        fg=cfg.TEXT_COLOR,
                                        activebackground=cfg.SUBCOLOR,
                                        activeforeground=cfg.TEXT_COLOR,
                                        selectcolor=cfg.MAIN_COLOR,
                                        state=DISABLED,
                                        command=self.onRadiobuttonChanged
                                        )
        self.fRadiobutton.place(x=100, y=127)

        self.gRadiobutton = Radiobutton(master=self.mainLabel,
                                        text='G',
                                        variable=self.changeFGVar,
                                        value=1,
                                        font='Arial 11',
                                        bg=cfg.SUBCOLOR,
                                        bd=0,
                                        fg=cfg.TEXT_COLOR,
                                        activebackground=cfg.SUBCOLOR,
                                        activeforeground=cfg.TEXT_COLOR,
                                        selectcolor=cfg.MAIN_COLOR,
                                        state=DISABLED,
                                        command=self.onRadiobuttonChanged
                                        )
        self.gRadiobutton.place(x=140, y=127)

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
     
