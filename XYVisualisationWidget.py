from tkinter import *
from tkinter import ttk
from config import Cfg as cfg
import math

def remap(old_value, old_min, old_max, new_min, new_max):
    out = ((old_value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
    if out > new_max:
        out = new_max
    elif out < new_min:
        out = new_min
    return out


class XYVisualisationWidget:

    mainLabel = None
    canvas = None
    canvasSize = 0

    displayMinX = 0
    displayMaxX = 0
    point_size = 5

    X = 210 * cfg.SIZE_MULT
    Y = 30 * cfg.SIZE_MULT
    WIDTH = 300 * cfg.SIZE_MULT
    HEIGHT = 280 * cfg.SIZE_MULT

    def __init__(self, main):

        self.main = main

        self.mainLabel = ttk.Frame(style="RoundedFrame", height=self.HEIGHT, width=self.WIDTH)
        self.mainLabel.place(x=self.X, y=self.Y)

        pad = 15
        pad_y = pad/2
        self.canvasSize = self.WIDTH-pad*2
        self.canvas = Canvas(master=self.mainLabel,
                             width=self.canvasSize,
                             height=self.canvasSize,
                             bg=cfg.SUBCOLOR,
                             highlightthickness=0)
        self.canvas.place(x=pad, y=pad_y)

        circle_size = self.canvasSize / 2
        self.displayMaxX = circle_size
        self.canvas.create_arc(self.canvasSize / 2 - circle_size,
                               self.canvasSize / 2 - circle_size,
                               self.canvasSize / 2 + circle_size,
                               self.canvasSize / 2 + circle_size,
                               fill=cfg.MAIN_COLOR,
                               outline=cfg.MAIN_COLOR,
                               start=cfg.ManipulatorConfig.Z_ANGLE_LIMIT[0],
                               extent=abs(cfg.ManipulatorConfig.Z_ANGLE_LIMIT[0])+cfg.ManipulatorConfig.Z_ANGLE_LIMIT[1])

        display_min_x = (cfg.ManipulatorConfig.LIMIT_X[0] / cfg.ManipulatorConfig.LIMIT_X[1]) * circle_size
        self.displayMinX = display_min_x
        self.canvas.create_arc(self.canvasSize / 2 - display_min_x,
                               self.canvasSize / 2 - display_min_x,
                               self.canvasSize / 2 + display_min_x,
                               self.canvasSize / 2 + display_min_x,
                               fill=cfg.SUBCOLOR,
                               outline=cfg.SUBCOLOR,
                               start=cfg.ManipulatorConfig.Z_ANGLE_LIMIT[0],
                               extent=abs(cfg.ManipulatorConfig.Z_ANGLE_LIMIT[0]) + cfg.ManipulatorConfig.Z_ANGLE_LIMIT[
                                   1])
        pos = self.toLocal(300, 0)

        self.canvas.create_oval(pos[0] - self.point_size,
                                pos[1] - self.point_size,
                                pos[0] + self.point_size,
                                pos[1] + self.point_size,
                                fill=cfg.TEXT_COLOR,
                                outline=cfg.TEXT_COLOR,
                                tag='point'
                                )



    def update(self, x=None, y=None):
        if x == None or y == None:
            x = float(self.main.controlPanelWidget.xEntry.get())
            y = float(self.main.controlPanelWidget.yEntry.get())
        x, y = self.toLocal(x, y)
        self.canvas.moveto('point', x-self.point_size, y-self.point_size)


    def toLocal(self, x, y):
        limitX = cfg.ManipulatorConfig.LIMIT_X
        limitY = cfg.ManipulatorConfig.LIMIT_Y

        out_x = self.canvasSize / 2 - math.copysign(remap(abs(x), 0, limitX[1], 0, self.displayMaxX), x)
        out_y = self.canvasSize / 2 + math.copysign(remap(abs(y), 0, limitY[1], 0, self.displayMaxX), y)
        return out_y, out_x






