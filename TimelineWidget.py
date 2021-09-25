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

    listX = []
    globalTag = None
    lastGlobalTag = None
    scrollX = 0

    def drawLines(self, seconds, pix_per_sec):
        for i in range(seconds):
            i += 1
            self.canvas.create_line(i*pix_per_sec, 30, i*pix_per_sec, 90, width=2, fill=cfg.LINE_COLOR)
            self.canvas.create_text(i*pix_per_sec, 10, text=str(i), fill=cfg.LINE_COLOR)

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
        self.canvas.bind("<Button-2>", self.create_point)
        self.canvas.bind("<B1-Motion>", self.move_point)
        self.root.bind("<Delete>", self.delete_point)
        self.root.bind("<Escape>", self.escape_point)

        self.drawLines(60, self.pixPerSecond)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"), xscrollincrement=ceil(self.canvas.bbox("all")[2] / 60))

    def _on_mousewheel(self, event):

        self.canvas.xview_scroll(int(copysign(1, event.delta)), UNITS)

        self.scrollX += copysign(ceil(self.canvas.bbox("all")[2] / 60), event.delta)

        if self.canvas.xview()[0] == 0:
            self.scrollX = 0
        elif self.canvas.xview()[1] == 1:
            self.scrollX = 2450

    def create_point(self, event):
        x = (self.scrollX + event.x)
        y = 60
        tag = "t"+str(x)

        self.canvas.create_polygon((x, y+5), (x+5, y), (x, y-5), (x-5, y), fill='orange', tag=tag)
        self.canvas.tag_bind(tag, "<Button-1>", lambda event: self.choose_point(tag))

    def choose_point(self, tag):
        self.globalTag = tag

        self.canvas.itemconfigure(self.lastGlobalTag, fill='orange')

        self.canvas.itemconfigure(self.globalTag, fill='red')
        self.escape_point()

    def escape_point(self, event=None):
        if self.lastGlobalTag == self.globalTag:
            self.canvas.itemconfigure(self.globalTag, fill='orange')
            self.globalTag = None
        self.lastGlobalTag = self.globalTag

    def move_point(self, event):
        try:
            x = event.x + self.scrollX
            y = 60

            self.canvas.coords(self.globalTag, x, y+5, x+5, y, x, y-5, x-5, y)
            print(self.canvas.coords(self.globalTag))
        except TclError:
            return

    def delete_point(self, event):
        self.canvas.delete(self.globalTag)
        self.canvas.tag_unbind(self.globalTag, "<Button-1>")
