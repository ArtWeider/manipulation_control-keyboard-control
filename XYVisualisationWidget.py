from tkinter import *
from tkinter import ttk
from config import Cfg as cfg


class XYVisualisationWidget:

    mainLabel = None
    canvas = None
    canvasSize = 0

    X = 210 * cfg.SIZE_MULT
    Y = 30 * cfg.SIZE_MULT
    WIDTH = 300 * cfg.SIZE_MULT
    HEIGHT = 280 * cfg.SIZE_MULT

    def __init__(self):

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
        self.canvas.create_arc(self.canvasSize / 2 - circle_size,
                               self.canvasSize / 2 - circle_size,
                               self.canvasSize / 2 + circle_size,
                               self.canvasSize / 2 + circle_size,
                               fill=cfg.MAIN_COLOR,
                               outline=cfg.MAIN_COLOR,
                               start=cfg.ManipulatorConfig.Z_ANGLE_LIMIT[0],
                               extent=abs(cfg.ManipulatorConfig.Z_ANGLE_LIMIT[0])+cfg.ManipulatorConfig.Z_ANGLE_LIMIT[1])

        display_min_x = (cfg.ManipulatorConfig.LIMIT_X[0] / cfg.ManipulatorConfig.LIMIT_X[1]) * circle_size
        print(display_min_x)
        self.canvas.create_arc(self.canvasSize / 2 - display_min_x,
                               self.canvasSize / 2 - display_min_x,
                               self.canvasSize / 2 + display_min_x,
                               self.canvasSize / 2 + display_min_x,
                               fill=cfg.SUBCOLOR,
                               outline=cfg.SUBCOLOR,
                               start=cfg.ManipulatorConfig.Z_ANGLE_LIMIT[0],
                               extent=abs(cfg.ManipulatorConfig.Z_ANGLE_LIMIT[0]) + cfg.ManipulatorConfig.Z_ANGLE_LIMIT[
                                   1])





