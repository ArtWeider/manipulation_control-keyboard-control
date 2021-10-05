from tkinter import *
from tkinter import ttk
from config import Cfg as cfg
from SaveClass import Save


class SavesWidget:

    main = None

    mainFrame = None
    titleLabel = None
    whiteLineFrame = None
    listBox = None
    scrollBar = None

    currentSave = Save()

    X = 5 * cfg.SIZE_MULT
    Y = 30 * cfg.SIZE_MULT
    WIDTH = 200 * cfg.SIZE_MULT
    HEIGHT = 365 * cfg.SIZE_MULT

    def __init__(self, main):

        self.main = main

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

        self.listBox.bind("<<ListboxSelect>>", self.onSelected)
        self.fillFromDict(main.savesManager.saves)

    def fillFromDict(self, dict):
        self.listBox.delete(0, END)
        for i in dict.keys():
            self.listBox.insert(0, i)

    def onSelected(self, event):
        if self.listBox.curselection() != ():
            selection = self.listBox.get(self.listBox.curselection())
            self.main.savesManager.currentSave = selection
            self.main.timelineWidget.drawSave()
            self.main.savesMenuWidget.onSaveSelected()

            save = self.main.savesManager.currentSave

            self.main.graphicWidget.point.points['x'] = []
            self.main.graphicWidget.point.points['y'] = []
            self.main.graphicWidget.point.points['z'] = []

            if len(self.main.savesManager.saves[save].points) != len(self.main.graphicWidget.point.points['x']):
                for time in self.main.savesManager.saves[save].points.keys():
                    self.main.graphicWidget.point.points['x'].append(self.main.savesManager.saves[save].points[time].x)
                    self.main.graphicWidget.point.points['y'].append(self.main.savesManager.saves[save].points[time].y)
                    self.main.graphicWidget.point.points['z'].append(self.main.savesManager.saves[save].points[time].z)
                    self.main.graphicWidget.point.points['time'].append(time)
        else:
            self.listBox.selection_set(self.listBox.get(0, END).index(self.main.savesManager.currentSave))








