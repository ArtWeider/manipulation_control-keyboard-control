from tkinter import *
from tkinter import ttk
from config import Cfg as cfg


def remap(old_value, old_min, old_max, new_min, new_max):
    out = ((old_value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
    if out > new_max:
        out = new_max
    elif out < new_min:
        out = new_min
    return out



class XZVisualisationWidget:

    mainLabel = None
    textLabel = None

    main = None

    X = 210 * cfg.SIZE_MULT
    Y = 315 * cfg.SIZE_MULT
    WIDTH = 300 * cfg.SIZE_MULT
    HEIGHT = 280 * cfg.SIZE_MULT

    def __init__(self, main):

        self.main = main

        self.mainLabel = ttk.Frame(style="RoundedFrame", height=self.HEIGHT, width=self.WIDTH)
        self.mainLabel.place(x=self.X, y=self.Y)

        self.canvas = Canvas(master=self.mainLabel,
                             bg=cfg.MAIN_COLOR,
                             width=self.WIDTH-20,
                             height=self.HEIGHT-20,
                             highlightthickness=0)
        self.canvas.place(x=10, y=10)

        pos = self.toLocal(400, 300)

        self.canvas.create_oval(pos[0]-5,
                                pos[1]-5,
                                pos[0]+5,
                                pos[1]+5,
                                fill=cfg.TEXT_COLOR,
                                tag='point')


    def toLocal(self, x, z):
        limitX = cfg.ManipulatorConfig.LIMIT_X
        limitZ = cfg.ManipulatorConfig.LIMIT_Z

        out_x = remap(x, limitX[0], limitX[1], 0, self.WIDTH-20)
        out_z = self.HEIGHT - remap(z, limitZ[0], limitZ[1], 0, self.HEIGHT-20)
        return out_x, out_z

    def update(self, x=None, z=None):
        if x == None or z == None:
            x = float(self.main.controlPanelWidget.xEntry.get())
            z = float(self.main.controlPanelWidget.zEntry.get())
        x, z = self.toLocal(x, z)
        self.canvas.moveto('point', x - 5, z - 5)



