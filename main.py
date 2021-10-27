from tkinter import *
from UpperStatusBarWidget import UpperStatusBar
from SavesWidget import SavesWidget
from config import Cfg as cfg
from tkinter import ttk
from PIL import Image, ImageTk
from PointMenuWidget import PointMenuWidget
from HandVisualisationWidget import HandVisualisationWidget
from SavesMenuWidget import SavesMenuWidget
from GraphicWidget import GraphicWidget
from TimelineWidget import TimelineWidget
from XYVisualisationWidget import XYVisualisationWidget
from XZVisualisationWidget import XZVisualisationWidget
from ControlPanelWidget import ControlPanelWidget
from SavesManager import SavesManager
from ManipulatorController import ManipulatorController
#import Tests.VoiceTest as Voice

class Main:

    root = None
    style = None

    savesManager = None
    manipulatorController = None

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

    def quit(self):
        self.root.destroy()
        self.matplotlibWidget.quit()
        exit()

    def __init__(self):
        self.root = Tk()
        self.style = ttk.Style()


        self.root.protocol("WM_DELETE_WINDOWS", self.quit)

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

        self.savesManager = SavesManager(self)
        self.manipulatorController = ManipulatorController(self)

        self.upperStatusBar = UpperStatusBar()
        self.savesWidget = SavesWidget(self)
        self.pointMenuWidget = PointMenuWidget(self)
        self.handVisualisationWidget = HandVisualisationWidget()
        self.savesMenuWidget = SavesMenuWidget(self)
        self.graphicWidget = GraphicWidget(self)
        self.timelineWidget = TimelineWidget(self)
        self.xyVisualisationWidget = XYVisualisationWidget(self)
        self.xzVisualisationWidget = XZVisualisationWidget()
        self.controlPanelWidget = ControlPanelWidget(self)
        #Voice.main = self

        self.root.mainloop()


if __name__ == "__main__":
    main = Main()
