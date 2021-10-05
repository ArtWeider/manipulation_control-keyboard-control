from tkinter import *
from tkinter import ttk
from config import Cfg as cfg
from math import *


class HandVisualisationWidget:

    mainLabel = None
    verticalLine = None
    handCanvas = None
    A1Label = None
    A2Label = None
    A3Label = None
    A4Label = None
    A5Label = None
    A6Label = None

    X = 5 * cfg.SIZE_MULT
    Y = 600 * cfg.SIZE_MULT
    WIDTH = 505 * cfg.SIZE_MULT
    HEIGHT = 295 * cfg.SIZE_MULT

    canvasSize = (WIDTH-(WIDTH/4) - 25, HEIGHT-20)

    def DrawHand(self, a1, a2, a3, l1, l2, l3):
        point_size = 5
        width = self.canvasSize[0]
        height = self.canvasSize[1]
        p1 = [10, height/2]
        p2 = self.GetPointPos(p1, l1, a1)
        p3 = self.GetPointPos(p2, l2, a2)
        p4 = self.GetPointPos(p3, l3, a3)

        self.handCanvas.create_line(p1[0],
                                    p1[1],
                                    p2[0],
                                    p2[1],
                                    width=5,
                                    fill=cfg.MAIN_COLOR)

        self.handCanvas.create_line(p2[0],
                                    p2[1],
                                    p3[0],
                                    p3[1],
                                    width=5,
                                    fill=cfg.MAIN_COLOR)

        self.handCanvas.create_line(p3[0],
                                    p3[1],
                                    p4[0],
                                    p4[1],
                                    width=5,
                                    fill=cfg.MAIN_COLOR)

        self.handCanvas.create_oval(p1[0]-point_size,
                                    p1[1]-point_size,
                                    p1[0]+point_size,
                                    p1[1]+point_size,
                                    fill=cfg.TEXT_COLOR,
                                    outline=cfg.TEXT_COLOR)

        self.handCanvas.create_oval(p2[0] - point_size,
                                    p2[1] - point_size,
                                    p2[0] + point_size,
                                    p2[1] + point_size,
                                    fill=cfg.TEXT_COLOR,
                                    outline=cfg.TEXT_COLOR)

        self.handCanvas.create_oval(p3[0] - point_size,
                                    p3[1] - point_size,
                                    p3[0] + point_size,
                                    p3[1] + point_size,
                                    fill=cfg.TEXT_COLOR,
                                    outline=cfg.TEXT_COLOR)

    def GetPointPos(self, sp, l, angle):

        out = [int(sp[0] + l * cos(radians(angle))), int(sp[1] + l * sin(radians(angle)))]
        return out

    def __init__(self):
        self.mainLabel = ttk.Frame(style="RoundedFrame", height=self.HEIGHT, width=self.WIDTH)
        self.mainLabel.place(x=self.X, y=self.Y)

        self.verticalLine = Frame(master=self.mainLabel,
                                  width=2,
                                  height=self.HEIGHT-8,
                                  bg=cfg.LINE_COLOR,

                                  )

        self.verticalLine.place(x=self.WIDTH-(self.WIDTH/4), y=4)

        self.handCanvas = Canvas(master=self.mainLabel,
                                 width=self.canvasSize[0],
                                 height=self.canvasSize[1],
                                 bg=cfg.SUBCOLOR,
                                 bd=0,
                                 relief=RIDGE,
                                 highlightthickness=0
                                 )
        self.handCanvas.place(x=10, y=10)

        self.A1Label = Label(
            master=self.mainLabel,
            text="A1: 25°",
            font="Arial 14",
            height=1,
            bg=cfg.SUBCOLOR,
            fg=cfg.TEXT_COLOR,
        )
        self.A1Label.place(x=self.WIDTH-(self.WIDTH/4)+5, y=12)

        self.A2Label = Label(
            master=self.mainLabel,
            text="A2: 5°",
            font="Arial 14",
            height=1,
            bg=cfg.SUBCOLOR,
            fg=cfg.TEXT_COLOR,
        )
        self.A2Label.place(x=self.WIDTH - (self.WIDTH / 4) + 5, y=44)

        self.A3Label = Label(
            master=self.mainLabel,
            text="A3: 15°",
            font="Arial 14",
            height=1,
            bg=cfg.SUBCOLOR,
            fg=cfg.TEXT_COLOR,
        )
        self.A3Label.place(x=self.WIDTH - (self.WIDTH / 4) + 5, y=76)

        self.A4Label = Label(
            master=self.mainLabel,
            text="A4: 174°",
            font="Arial 14",
            height=1,
            bg=cfg.SUBCOLOR,
            fg=cfg.TEXT_COLOR,
        )
        self.A4Label.place(x=self.WIDTH - (self.WIDTH / 4) + 5, y=107)

        self.A5Label = Label(
            master=self.mainLabel,
            text="A5: -85°",
            font="Arial 14",
            height=1,
            bg=cfg.SUBCOLOR,
            fg=cfg.TEXT_COLOR,
        )
        self.A5Label.place(x=self.WIDTH - (self.WIDTH / 4) + 5, y=139)

        self.A6Label = Label(
            master=self.mainLabel,
            text="A6: 76%",
            font="Arial 14",
            height=1,
            bg=cfg.SUBCOLOR,
            fg=cfg.TEXT_COLOR,
        )
        self.A6Label.place(x=self.WIDTH - (self.WIDTH / 4) + 5, y=169)

        self.DrawHand(25, 5, 15, 80, 70, 40)








