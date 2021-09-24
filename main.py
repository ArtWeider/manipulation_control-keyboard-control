from tkinter import *
from UpperStatusBarWidget import UpperStatusBar
from SavesWidget import SavesWidget
from config import Cfg as cfg
from tkinter import ttk
from PIL import Image, ImageTk
from PointMenuWidget import PointMenuWidget
from HandVisualisationWidget import HandVisualisationWidget
from SavesMenuWidget import SavesMenuWidget
from MatplotlibWidget import MatplotlibWidget
from TimelineWidget import TimelineWidget
from XYVisualisationWidget import XYVisualisationWidget
from XZVisualisationWidget import XZVisualisationWidget
from ControlPanelWidget import ControlPanelWidget
from SavesManager import SavesManager


class Main:

    root = None
    style = None

    savesManager = None

    upperStatusBar = None
    savesWidget = None
    pointMenuWidget = None
    handVisualisationWidget = None
    savesMenuWidget = None
    matplotlibWidget = None
    timelineWidget = None
    xyVisualisationWidget = None
    xzVisualisationWidget = None
    controlPanelWidget = None

    def __init__(self):
        self.root = Tk()
        self.style = ttk.Style()

        _image = Image.open("Images/RoundedImage.png")
        borderImage = ImageTk.PhotoImage(_image)
        self.style.element_create("RoundedFrame",
                     "image", borderImage,
                     border=16, sticky="nsew")
        self.style.layout("RoundedFrame",
                     [("RoundedFrame", {"sticky": "nsew"})])

        self.root.title(cfg.WINDOW_NAME)
        self.root.geometry(cfg.SIZE)
        self.root.resizable(width=False, height=False)

        self.root.configure(bg=cfg.MAIN_COLOR)

        self.savesManager = SavesManager()

        self.upperStatusBar = UpperStatusBar()
        self.savesWidget = SavesWidget(self)
        self.pointMenuWidget = PointMenuWidget()
        self.handVisualisationWidget = HandVisualisationWidget()
        self.savesMenuWidget = SavesMenuWidget()
        self.matplotlibWidget = MatplotlibWidget(self.root)
        self.timelineWidget = TimelineWidget(self)
        self.xyVisualisationWidget = XYVisualisationWidget()
        self.xzVisualisationWidget = XZVisualisationWidget()
        self.controlPanelWidget = ControlPanelWidget()

        self.root.mainloop()


if __name__ == "__main__":
    main = Main()