from tkinter import *
from tkinter import ttk
from config import Cfg as cfg


class ControlPanelWidget:

    main = None

    mainLabel = None
    textLabel = None

    X = 1320 * cfg.SIZE_MULT
    Y = 345 * cfg.SIZE_MULT
    WIDTH = 275 * cfg.SIZE_MULT
    HEIGHT = 550 * cfg.SIZE_MULT

    def setStateAll(self, state):
        self.xLabel.configure(state=state)
        self.yLabel.configure(state=state)
        self.zLabel.configure(state=state)
        self.qLabel.configure(state=state)
        self.eLabel.configure(state=state)
        self.fLabel.configure(state=state)
        self.qSlider.configure(state=state)
        self.eSlider.configure(state=state)
        self.fSlider.configure(state=state)
        self.takeSpongeButton.configure(state=state)
        self.takeBoltButton.configure(state=state)
        self.takeMarkerButton.configure(state=state)
        self.playButton.configure(state=state)
        self.pauseButton.configure(state=state)

    def onScaleChanged(self, event, slider):

        if slider == 'q':
            angle = (self.qSlider.get() / 100) * cfg.ManipulatorConfig.Q_LIMIT[1]
            self.main.manipulatorController.goToPoint(q=angle)
            self.qLabel.configure(text=f"Q: {str(int(angle))}")
        elif slider == 'e':
            #angle = (self.eSlider.get() / 100) * cfg.ManipulatorConfig.Q_LIMIT[1]
            angle = self.eSlider.get()
            #self.main.manipulatorController.goToPoint(q=angle)
            self.eLabel.configure(text=f"E: {str(int(angle))}")
        elif slider == 'f':
            #angle = (self.eSlider.get() / 100) * cfg.ManipulatorConfig.Q_LIMIT[1]
            angle = self.fSlider.get()
            #self.main.manipulatorController.goToPoint(q=angle)
            self.fLabel.configure(text=f"F: {str(int(angle))}")

    def onIPEnterPressed(self, event):
        self.main.manipulatorController.connect(self.IPEntry.get())
        if self.main.manipulatorController.connected:
            self.setStateAll(NORMAL)
        else:
            self.setStateAll(DISABLED)


    def onEnterPressed(self, event):
        x = float(self.xEntry.get())
        y = float(self.yEntry.get())
        z = float(self.zEntry.get())
        q = (float(self.qSlider.get()) / 100) * cfg.ManipulatorConfig.Q_LIMIT[1]
        print('debug 3')
        self.main.manipulatorController.goToPoint(False, x=x, y=y, z=z, q=q)

    def __init__(self, main):

        self.main = main

        self.mainLabel = ttk.Frame(style="RoundedFrame", height=self.HEIGHT, width=self.WIDTH)
        self.mainLabel.place(x=self.X, y=self.Y)

        self.textLabel = Label(
            master=self.mainLabel,
            text="Манипулятор",
            font="Arial 11",
            height=1,
            bg=cfg.SUBCOLOR,
            fg=cfg.TEXT_COLOR,
        )
        self.textLabel.place(x=50, y=4)

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

        self.qSlider = Scale(master=self.mainLabel,
                             orient=HORIZONTAL,
                             showvalue=False,
                             length=120,
                             bg=cfg.LINE_COLOR,
                             activebackground=cfg.LINE_COLOR,
                             bd=0,
                             fg=cfg.MAIN_COLOR,
                             highlightthicknes=0,
                             sliderrelief=FLAT,
                             width=7,
                             highlightbackground=cfg.SUBCOLOR,
                             highlightcolor=cfg.MAIN_COLOR,
                             relief=FLAT,
                             troughcolor=cfg.MAIN_COLOR,
                             command=lambda event: self.onScaleChanged(event, 'q'))
        self.qSlider.place(x=60, y=75)

        self.eLabel = Label(master=self.mainLabel,
                            text="E: ",
                            font="Arial 11",
                            height=1,
                            bg=cfg.SUBCOLOR,
                            fg=cfg.TEXT_COLOR)
        self.eLabel.place(x=5, y=97)

        self.eSlider = Scale(master=self.mainLabel,
                             orient=HORIZONTAL,
                             showvalue=False,
                             length=120,
                             bg=cfg.LINE_COLOR,
                             activebackground=cfg.LINE_COLOR,
                             bd=0,
                             fg=cfg.MAIN_COLOR,
                             highlightthicknes=0,
                             sliderrelief=FLAT,
                             width=7,
                             highlightbackground=cfg.SUBCOLOR,
                             highlightcolor=cfg.MAIN_COLOR,
                             relief=FLAT,
                             troughcolor=cfg.MAIN_COLOR,
                             command=lambda event: self.onScaleChanged(event, 'e'))
        self.eSlider.place(x=60, y=105)

        self.fLabel = Label(master=self.mainLabel,
                             text="F: ",
                             font="Arial 11",
                             height=1,
                             bg=cfg.SUBCOLOR,
                             fg=cfg.TEXT_COLOR)
        self.fLabel.place(x=5, y=127)

        self.fSlider = Scale(master=self.mainLabel,
                              orient=HORIZONTAL,
                              showvalue=False,
                              length=120,
                              bg=cfg.LINE_COLOR,
                              activebackground=cfg.LINE_COLOR,
                              bd=0,
                              fg=cfg.MAIN_COLOR,
                              highlightthicknes=0,
                              sliderrelief=FLAT,
                              width=7,
                              highlightbackground=cfg.SUBCOLOR,
                              highlightcolor=cfg.MAIN_COLOR,
                              relief=FLAT,
                              troughcolor=cfg.MAIN_COLOR,
                             command=lambda event: self.onScaleChanged(event, 'f'))
        self.fSlider.place(x=60, y=135)

        self.IPLabel = Label(master=self.mainLabel,
                             text="Адрес: ",
                             font="Arial 11",
                             height=1,
                             bg=cfg.SUBCOLOR,
                             fg=cfg.TEXT_COLOR)
        self.IPLabel.place(x=5, y=158)

        self.IPEntry = Entry(width=15,
                            master=self.mainLabel,
                            font='Arial 11',
                            bg=cfg.SUBCOLOR,
                            bd=0,
                            fg=cfg.TEXT_COLOR,
                            justify=LEFT,
                            disabledbackground=cfg.SUBCOLOR)
        self.IPEntry.place(x=60, y=160)
        self.IPEntry.bind("<Return>", self.onIPEnterPressed)
        self.IPEntry.insert(0, cfg.ManipulatorConfig.DEFAULT_NAME)

        self.takeMarkerButton = Button(master=self.mainLabel,
                                         text="Взять маркер",
                                         bg=cfg.BUTTON_COLOR,
                                         bd=0,
                                         fg=cfg.TEXT_COLOR,
                                         width=24,
                                         activebackground=cfg.BUTTON_ACTIVE_COLOR,
                                         activeforeground=cfg.TEXT_COLOR,
                                         )
        self.takeMarkerButton.place(x=11, y=190)

        self.takeSpongeButton = Button(master=self.mainLabel,
                                       text="Взять губку",
                                       bg=cfg.BUTTON_COLOR,
                                       bd=0,
                                       fg=cfg.TEXT_COLOR,
                                       width=24,
                                       activebackground=cfg.BUTTON_ACTIVE_COLOR,
                                       activeforeground=cfg.TEXT_COLOR,
                                       )
        self.takeSpongeButton.place(x=11, y=220)

        self.takeBoltButton = Button(master=self.mainLabel,
                                       text="Взять болт",
                                       bg=cfg.BUTTON_COLOR,
                                       bd=0,
                                       fg=cfg.TEXT_COLOR,
                                       width=24,
                                       activebackground=cfg.BUTTON_ACTIVE_COLOR,
                                       activeforeground=cfg.TEXT_COLOR,
                                       )
        self.takeBoltButton.place(x=11, y=250)

        self.playButton = Button(master=self.mainLabel,
                                     text="Запустить",
                                     bg=cfg.BUTTON_COLOR,
                                     bd=0,
                                     fg=cfg.TEXT_COLOR,
                                     width=24,
                                     activebackground=cfg.BUTTON_ACTIVE_COLOR,
                                     activeforeground=cfg.TEXT_COLOR,
                                     command=lambda: self.main.manipulatorController.play(self.main.savesManager.saves[self.main.savesManager.currentSave])
                                     )
        self.playButton.place(x=11, y=280)

        self.pauseButton = Button(master=self.mainLabel,
                                 text="Пауза",
                                 bg=cfg.BUTTON_COLOR,
                                 bd=0,
                                 fg=cfg.TEXT_COLOR,
                                 width=24,
                                 activebackground=cfg.BUTTON_ACTIVE_COLOR,
                                 activeforeground=cfg.TEXT_COLOR,
                                 command=self.main.manipulatorController.pause,
                                 )
        self.pauseButton.place(x=11, y=310)

        if self.main.manipulatorController.connected:
            self.setStateAll(NORMAL)
        else:
            self.setStateAll(DISABLED)



