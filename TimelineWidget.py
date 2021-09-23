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

    scrollX = 0

    def _on_mousewheel(self, event):
        self.canvas.xview_scroll(int(copysign(1, -event.delta)), "units")
        self.scrollX += copysign(ceil(self.canvas.bbox("all")[2] / 60), -event.delta)

        if self.scrollX < 0:
            self.scrollX = 0
        elif self.scrollX > 2450:
            self.scrollX = 2450

        print(self.scrollX)

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

        # self.canvas.xscrollincrement = self.canvas.bbox("all")[2]

        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Double-Button-1>", self.create_point)

        for i in range(60):
            self.canvas.create_line(i*50, 30, i*50, 90, width=2, fill=cfg.LINE_COLOR)
            self.canvas.create_text(i*50, 10, text=str(i+1), fill=cfg.LINE_COLOR)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"), xscrollincrement=ceil(self.canvas.bbox("all")[2] / 60))

    def create_point(self, event):
        x = (self.scrollX + (event.widget.winfo_pointerx() - event.widget.winfo_rootx()))
        y = 60
        self.canvas.create_polygon((x, y+5), (x+5, y), (x, y-5), (x-5, y), fill='orange')




