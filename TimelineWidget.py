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

    scrollX = 0

    def _on_mousewheel(self, event):

        if self.canvas.xview()[0] == 0:
            self.scrollX = 0
        elif self.canvas.xview()[1] == 1:
            self.scrollX = 2450
        else:
            self.scrollX += copysign(ceil(self.canvas.bbox("all")[2] / 60), event.delta)
        print(self.scrollX)
        self.canvas.xview_scroll(int(copysign(1, event.delta)), UNITS)

    def __init__(self, root):

        self.root = root

        self.mainLabel = ttk.Frame(style="RoundedFrame", height=self.HEIGHT, width=self.WIDTH)
        self.mainLabel.place(x=self.X, y=self.Y)

        self.canvas = Canvas(master=self.mainLabel,
                             width=self.WIDTH - 20,
                             height=self.HEIGHT - 20,
                             bg=cfg.MAIN_COLOR,
                             highlightthickness=0
                             )
        self.canvas.place(x=10, y=10)

        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Double-Button-1>", self.create_point)

        self.drawLines(60, self.pixPerSecond)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"), xscrollincrement=ceil(self.canvas.bbox("all")[2] / 60))


    def create_point(self, event):
        x = (self.scrollX + (event.widget.winfo_pointerx() - event.widget.winfo_rootx()))
        y = 60
        self.canvas.create_polygon((x, y+5), (x+5, y), (x, y-5), (x-5, y), fill='orange')

    def _create_point(self, event):
        bbox = self.canvas.bbox("all")
        xview = self.canvas.xview()
        len = bbox[2] - bbox[0]
        start_x = bbox[0] + len * xview[0]
        end_x = bbox[0] + len * xview[1]

        print(f"bbox: {bbox[0], bbox[2]}, xview: {xview}, start_x: {start_x}, end_x: {end_x}")
        x = (start_x + (event.widget.winfo_pointerx() - event.widget.winfo_rootx()))
        y = 60
        self.canvas.create_polygon((x, y + 5), (x + 5, y), (x, y - 5), (x - 5, y), fill='orange')

    def drawLines(self, seconds, pix_per_sec):
        for i in range(seconds):
            i+=1
            self.canvas.create_line(i*pix_per_sec, 30, i*pix_per_sec, 90, width=2, fill=cfg.LINE_COLOR)
            self.canvas.create_text(i*pix_per_sec, 10, text=str(i), fill=cfg.LINE_COLOR)
