from tkinter import *
from tkinter import ttk
from config import Cfg as cfg
from math import *

def remap(old_value, old_min, old_max, new_min, new_max):
    out = ((old_value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
    if out > new_max:
        out = new_max
    elif out < new_min:
        out = new_min
    return out

class TimelineWidget:

    root = None
    mainLabel = None
    canvas = None

    X = 515 * cfg.SIZE_MULT
    Y = 735 * cfg.SIZE_MULT
    WIDTH = 800 * cfg.SIZE_MULT
    HEIGHT = 160 * cfg.SIZE_MULT

    pixPerSecond = 50

    maxSeconds = 0

    def __init__(self, main):

        self.main = main

        self.mainLabel = ttk.Frame(style="RoundedFrame", height=self.HEIGHT, width=self.WIDTH)
        self.mainLabel.place(x=self.X, y=self.Y)

        self.canvas = Canvas(master=self.mainLabel,
                             width=self.WIDTH - 20,
                             height=self.HEIGHT - 20,
                             bg=cfg.MAIN_COLOR,
                             highlightthickness=0
                             )
        self.canvas.place(x=10, y=10)

        self.canvas.bind("<MouseWheel>", self.onMousewheel)
        self.canvas.bind("<Double-Button-1>", self.onMouseDoubleclicked)

        self.drawLines(0)

        self.canvas.configure(scrollregion=(0, 0, 50, 0), xscrollincrement=50)


    def onMouseDoubleclicked(self, event):
        x = self.canvas.canvasx(event.widget.winfo_pointerx() - event.widget.winfo_rootx())
        self.main.savesManager.currentSave.addPoint(x/self.pixPerSecond)
        self.addPointToTimeline(x)

    def onMousewheel(self, event):
        self.canvas.xview_scroll(int(copysign(1, event.delta)), UNITS)

    def drawPoint(self, x):
        y = 60
        self.canvas.create_polygon((x, y + 5), (x + 5, y), (x, y - 5), (x - 5, y), fill='orange')

    def drawLines(self, seconds, start_sec=0):
        if seconds <= 0:
            self.canvas.create_line(0, 0, 0, 0)
            return
        for i in range(start_sec, seconds+start_sec):
            i += 1
            self.canvas.create_line(i*self.pixPerSecond, 30, i*self.pixPerSecond, 90, width=2, fill=cfg.LINE_COLOR)
            self.canvas.create_text(i*self.pixPerSecond, 10, text=str(i), fill=cfg.LINE_COLOR)
        if start_sec+seconds > self.maxSeconds:
            self.maxSeconds = start_sec+seconds
        self.recalculateScrollLimits()

    def drawSave(self):
        self.canvas.delete(ALL)
        save = self.main.savesManager.currentSave
        self.maxSeconds = int(max(save.points.keys()))
        self.drawLines(self.maxSeconds + 5)
        for point in save.points.values():
            self.drawPoint(point.time * self.pixPerSecond)
        self.recalculateScrollLimits()

    def recalculateScrollLimits(self):
        scrollregion = list(self.canvas.bbox("all"))
        scrollregion[0] = 0
        if scrollregion[2] < 550:
            scrollregion[2] = 550
        self.canvas.configure(scrollregion=scrollregion)

    def addPointToTimeline(self, x):
        _sec = x // self.pixPerSecond
        if _sec > self.maxSeconds - 5:
            self.drawLines(self.maxSeconds, int(_sec - (self.maxSeconds - 5)))
        self.drawPoint(x)