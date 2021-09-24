from tkinter import *
from tkinter import ttk
from config import Cfg as cfg
from math import *


class TimelineWidget:

    root = None
    mainLabel = None
    canvas = None

    X = 515 * cfg.SIZE_MULT
    Y = 735 * cfg.SIZE_MULT
    WIDTH = 800 * cfg.SIZE_MULT
    HEIGHT = 160 * cfg.SIZE_MULT

    pixPerSecond = 50

    scrollXLimit = (0, 2500)
    scrollX = 0

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

        self.drawLines(60, self.pixPerSecond)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"), xscrollincrement=ceil(self.canvas.bbox("all")[2] / 60))


    def onMouseDoubleclicked(self, event):
        x = (self.scrollX + (event.widget.winfo_pointerx() - event.widget.winfo_rootx()))
        self.drawPoint(x)

    def onMousewheel(self, event):
        self.scrollX += copysign(ceil(self.canvas.bbox("all")[2] / 60), event.delta)

        if self.scrollX < self.scrollXLimit[0]:
            self.scrollX = self.scrollXLimit[0]
        elif self.scrollX > self.scrollXLimit[1]:
            self.scrollX = self.scrollXLimit[1]

        self.canvas.xview_scroll(int(copysign(1, event.delta)), UNITS)

    def drawPoint(self, x):
        y = 60
        self.canvas.create_polygon((x, y + 5), (x + 5, y), (x, y - 5), (x - 5, y), fill='orange')

    def drawLines(self, seconds, pix_per_sec):
        if seconds <= 0:
            self.canvas.create_line(0, 0, 0, 0)
            return
        for i in range(seconds):
            i += 1
            self.canvas.create_line(i*pix_per_sec, 30, i*pix_per_sec, 90, width=2, fill=cfg.LINE_COLOR)
            self.canvas.create_text(i*pix_per_sec, 10, text=str(i), fill=cfg.LINE_COLOR)
