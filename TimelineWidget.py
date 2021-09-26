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

    currentPoint = ['', '']

    tag2time = {}

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
        self.canvas.bind("<B1-Motion>", self.onLeftButtonMove)
        self.main.root.bind("<Delete>", self.onDeletePressed)
        self.main.root.bind("<Escape>", self.onEscPressed)

        self.drawLines(0)

        self.canvas.configure(scrollregion=(0, 0, 50, 0), xscrollincrement=50)


    def onMouseDoubleclicked(self, event):
        x = self.canvas.canvasx(event.widget.winfo_pointerx() - event.widget.winfo_rootx())
        self.main.savesManager.saves[self.main.savesManager.currentSave].addPoint(x/self.pixPerSecond)
        self.addPointToTimeline(x)

    def onEscPressed(self, event):
        self.deselectPoint()

    def deselectPoint(self):
        self.canvas.itemconfigure(self.currentPoint[1], fill=cfg.POINT_COLOR)
        self.currentPoint = ['', '']

    def onMousewheel(self, event):
        self.canvas.xview_scroll(int(copysign(1, event.delta)), UNITS)

    def onDeletePressed(self, event):
        self.deletePoint(self.currentPoint[1])

    def deletePoint(self, tag):
        time = self.tag2time[int(tag[1::])]
        del self.main.savesManager.saves[self.main.savesManager.currentSave].points[time]
        print(self.main.savesManager.saves[self.main.savesManager.currentSave].points)
        self.currentPoint = ['', '']
        self.canvas.delete(tag)
        self.canvas.tag_unbind(tag, "<Button-1>")

    def drawPoint(self, x):
        y = 60
        try:
            num = max(self.tag2time.keys())+1
        except ValueError:
            num = 0
        tag = f't{num}'
        self.tag2time[num] = x / self.pixPerSecond
        self.canvas.create_polygon((x, y + 5), (x + 5, y), (x, y - 5), (x - 5, y), fill=cfg.POINT_COLOR, tag=tag)
        self.canvas.tag_bind(tag, '<Button-1>', lambda event: self.onPointSelected(tag))

    def drawLines(self, seconds, start_sec=0):
        print(start_sec)
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
        self.currentPoint = ['', '']
        save = self.main.savesManager.saves[self.main.savesManager.currentSave]
        self.maxSeconds = int(max(save.points.keys()))
        self.drawLines(self.maxSeconds + 5)
        for point in save.points.values():
            self.drawPoint(point.time * self.pixPerSecond)
        self.recalculateScrollLimits()

    def onLeftButtonMove(self, event):
        x = self.canvas.canvasx(event.x)
        self.movePoint(self.currentPoint[1], x)

    def movePoint(self, tag, x):
        oldTime = self.tag2time[int(tag[1::])]
        newTime = x / self.pixPerSecond
        intTag = int(tag[1::])
        self.main.savesManager.saves[self.main.savesManager.currentSave].points[oldTime].time = newTime
        self.main.savesManager.saves[self.main.savesManager.currentSave].points[newTime] = self.main.savesManager.saves[self.main.savesManager.currentSave].points.pop(oldTime)
        self.tag2time[intTag] = newTime
        y=60
        self.canvas.coords(tag, x, y+5, x+5, y, x, y-5, x-5, y)


    def onPointSelected(self, tag):
        self.currentPoint[0] = self.currentPoint[1]
        self.currentPoint[1] = tag
        self.canvas.itemconfigure(self.currentPoint[0], fill=cfg.POINT_COLOR)
        self.canvas.itemconfigure(tag, fill=cfg.POINT_SELECTED_COLOR)

    def recalculateScrollLimits(self):
        scrollregion = list(self.canvas.bbox("all"))
        scrollregion[0] = 0
        if scrollregion[2] < 550:
            scrollregion[2] = 550
        self.canvas.configure(scrollregion=scrollregion)

    def addPointToTimeline(self, x):
        _sec = x // self.pixPerSecond
        if _sec > self.maxSeconds - 5:
            print(_sec, self.maxSeconds)
            self.drawLines(int(_sec - (self.maxSeconds - 5)), self.maxSeconds)
        self.drawPoint(x)
        num = max(self.tag2time.keys())
        self.onPointSelected(f"t{num}")

    def inMouseOnWidget(self, event):
        return event.x > self.X and event.x < self.X + self.WIDTH and event.y > self.Y and event.y < self.Y + self.HEIGHT

    def isSaveSelected(self):
        return self.main.savesManager.currentSave != None
