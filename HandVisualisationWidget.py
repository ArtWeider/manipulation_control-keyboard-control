from tkinter import *
from tkinter import ttk
from config import Cfg as cfg
import serial.tools.list_ports
import threading
from math import *

def remap(old_value, old_min, old_max, new_min, new_max):
    out = ((old_value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
    if out > new_max:
        out = new_max
    elif out < new_min:
        out = new_min
    return out


class HandVisualisationWidget:
    X = 5 * cfg.SIZE_MULT
    Y = 600 * cfg.SIZE_MULT
    WIDTH = 505 * cfg.SIZE_MULT
    HEIGHT = 295 * cfg.SIZE_MULT

    canvasSize = (WIDTH - (WIDTH / 2.5), HEIGHT - 20)

    ser = serial.Serial()
    portList = serial.tools.list_ports.comports()
    comPort = ''

    gloveData = {'sy': 0, 'sz': 0, 'wy': 0, 'hy': 0, 'hx': 0, 'g': 0}

    def DrawHand(self):

        if not self.main.manipulatorController.useHand:
            return

        point_size = 5
        width = self.canvasSize[0]
        height = self.canvasSize[1]

        shoulder_len = 80
        wrist_len = 70
        hand_len = 40

        real_shoulder_len = 250
        real_wrist_len = 240
        real_hand_len = 180

        start = [10, height / 2]
        shoulder = self.GetPointPos(start, shoulder_len, self.gloveData['sy'])
        wrist = self.GetPointPos(shoulder, wrist_len, self.gloveData['wy'])
        hand = self.GetPointPos(wrist, hand_len, self.gloveData['hy'])

        self.handCanvas.coords('l0', start[0], start[1], shoulder[0], shoulder[1])
        self.handCanvas.coords('l1', shoulder[0], shoulder[1], wrist[0], wrist[1])
        self.handCanvas.coords('l2', wrist[0], wrist[1], hand[0], hand[1])

        self.handCanvas.coords('p0', start[0] - point_size,
                                    start[1] - point_size,
                                    start[0] + point_size,
                                    start[1] + point_size)
        self.handCanvas.coords('p1', shoulder[0] - point_size,
                                    shoulder[1] - point_size,
                                    shoulder[0] + point_size,
                                    shoulder[1] + point_size)
        self.handCanvas.coords('p2', wrist[0] - point_size,
                                    wrist[1] - point_size,
                                    wrist[0] + point_size,
                                    wrist[1] + point_size)

        self.main.controlPanelWidget.xEntry.delete(0, END)
        self.main.controlPanelWidget.yEntry.delete(0, END)
        self.main.controlPanelWidget.zEntry.delete(0, END)

        x, z = self.GetPointPos(start, real_shoulder_len, self.gloveData['sy'])
        x, z = self.GetPointPos((x, z), real_wrist_len, self.gloveData['wy'])
        x, z = self.GetPointPos((x, z), real_hand_len, self.gloveData['hy'])
        x, y = self.GetPointPos((start[0], 0), x, self.gloveData['sz'])

        z = int(z / -2.2 + 300)
        # если не сработает поменять x и y местами
        x = int(x / 1.36)
        y = int(y / 1.36)


        self.main.controlPanelWidget.xEntry.insert(0, int(x))
        self.main.controlPanelWidget.yEntry.insert(0, int(y))
        self.main.controlPanelWidget.zEntry.insert(0, int(z))

        q = -int(self.gloveData['hy'] - 90)

        self.main.controlPanelWidget.qSlider.set((q / cfg.ManipulatorConfig.Q_LIMIT[1]) * 100)

        self.main.controlPanelWidget.qLabel.configure(text=f"Q: {q}")

        self.main.manipulatorController.goToPoint(x=x, y=y, z=z, q=q)

    def GetPointPos(self, startPoint, length, angle):

        out = [int(startPoint[0] + length * cos(radians(angle))), int(startPoint[1] + length * sin(radians(angle)))]
        return out


    def connectToUART(self):
        # поиск порта подключенного устройства
        for i in range(0, len(self.portList)):
            port = str(self.portList[i])
            if 'Silicon Labs' in port:
                self.comPort = (port.split(' ')[0])
                break
        if self.comPort != '':
            self.ser.port = self.comPort
            self.ser.baudrate = 9600
            self.ser.timeout = 1
            self.ser.open()
            print("Connected to " + self.comPort)
            self.main.manipulatorController.useHand = True

            return True
        else:
            return False

    def getDataFromGlove(self):
        while True:
            try:
                if self.ser.in_waiting:
                    packet = self.ser.readline().decode('utf-8').split('/')

                    self.A1Label['text'] = "S:" + packet[0] + "°"
                    self.A2Label['text'] = "W:" + packet[2] + "°"
                    self.A3Label['text'] = "H:" + packet[3] + "°"
                    self.A4Label['text'] = "YAW:" + packet[1] + "°"
                    self.A5Label['text'] = "ROLL:" + packet[4] + "°"
                    self.A6Label['text'] = "GRAB:" + packet[5] + "%"

                    self.gloveData['sy'] = float(packet[0])
                    self.gloveData['sz'] = float(packet[1])

                    self.gloveData['wy'] = float(packet[2])

                    self.gloveData['hy'] = float(packet[3])
                    self.gloveData['hx'] = float(packet[4])

                    self.gloveData['g'] = float(packet[5])

                    self.DrawHand()

            except UnicodeDecodeError: continue
            except ValueError: continue
            except IndexError: continue
            except RuntimeError: continue


    def __init__(self, main):
        self.main = main
        self.mainLabel = ttk.Frame(style="RoundedFrame", height=self.HEIGHT, width=self.WIDTH)
        self.mainLabel.place(x=self.X, y=self.Y)

        self.verticalLine = Frame(master=self.mainLabel,
                                  width=2,
                                  height=self.HEIGHT - 8,
                                  bg=cfg.LINE_COLOR)

        self.verticalLine.place(x=self.WIDTH - (self.WIDTH / 3) - 5, y=4)

        self.handCanvas = Canvas(master=self.mainLabel,
                                 width=self.canvasSize[0],
                                 height=self.canvasSize[1],
                                 bg=cfg.SUBCOLOR,
                                 bd=0,
                                 relief=RIDGE,
                                 highlightthickness=0)

        self.handCanvas.place(x=10, y=10)

        self.A1Label = Label(
            master=self.mainLabel,
            font="Arial 14",
            height=1,
            bg='FireBrick',
            fg=cfg.TEXT_COLOR)

        self.A1Label.place(x=self.WIDTH - (self.WIDTH / 3), y=12)

        self.A2Label = Label(
            master=self.mainLabel,
            font="Arial 14",
            height=1,
            bg='ForestGreen',
            fg=cfg.TEXT_COLOR)

        self.A2Label.place(x=self.WIDTH - (self.WIDTH / 3), y=44)

        self.A3Label = Label(
            master=self.mainLabel,
            font="Arial 14",
            height=1,
            bg='Teal',
            fg=cfg.TEXT_COLOR)
        self.A3Label.place(x=self.WIDTH - (self.WIDTH / 3), y=76)

        self.A4Label = Label(
            master=self.mainLabel,
            font="Arial 14",
            height=1,
            bg=cfg.SUBCOLOR,
            fg=cfg.TEXT_COLOR)

        self.A4Label.place(x=self.WIDTH - (self.WIDTH / 3), y=107)

        self.A5Label = Label(
            master=self.mainLabel,
            font="Arial 14",
            height=1,
            bg=cfg.SUBCOLOR,
            fg=cfg.TEXT_COLOR)

        self.A5Label.place(x=self.WIDTH - (self.WIDTH / 3), y=139)

        self.A6Label = Label(
            master=self.mainLabel,
            font="Arial 14",
            height=1,
            bg=cfg.SUBCOLOR,
            fg=cfg.TEXT_COLOR)

        self.A6Label.place(x=self.WIDTH - (self.WIDTH / 3), y=169)

        if self.connectToUART():

            self.handCanvas.create_line(0, 0, 1, 1, width=5, fill='FireBrick', tag='l0')
            self.handCanvas.create_line(0, 0, 1, 1, width=5, fill='ForestGreen', tag='l1')
            self.handCanvas.create_line(0, 0, 1, 1, width=5, fill='Teal', tag='l2')

            self.handCanvas.create_oval(0, 0, 1, 1, fill='SlateGray', outline='SlateGray', tag='p0')
            self.handCanvas.create_oval(0, 0, 1, 1, fill='SlateGray', outline='SlateGray', tag='p1')
            self.handCanvas.create_oval(0, 0, 1, 1, fill='SlateGray', outline='SlateGray', tag='p2')

            threading.Thread(target=self.getDataFromGlove).start()
