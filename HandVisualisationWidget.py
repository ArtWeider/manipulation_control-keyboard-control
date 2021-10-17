from tkinter import *
from tkinter import ttk
from config import Cfg as cfg
import serial.tools.list_ports
import threading
from math import *
from time import sleep


class HandVisualisationWidget:
    X = 5 * cfg.SIZE_MULT
    Y = 600 * cfg.SIZE_MULT
    WIDTH = 505 * cfg.SIZE_MULT
    HEIGHT = 295 * cfg.SIZE_MULT

    canvasSize = (WIDTH - (WIDTH / 2.5), HEIGHT - 20)

    ser = serial.Serial()
    portList = serial.tools.list_ports.comports()
    comPort = ''

    gloveData = {'sy': 0, 'sz': 0, 'X': 0, 'Y': 0, 'Z': 0, 'wy': 0, 'hy': 0, 'hx': 0, 'g': 0}

    def DrawHand(self):
        point_size = 5
        width = self.canvasSize[0]
        height = self.canvasSize[1]

        shoulder_len = 80
        wrist_len = 70
        hand_len = 40

        while True:
            try:
                start = [0, 0] #[10, height / 2]
                shoulder = self.GetPointPos(start, shoulder_len, self.gloveData['sy'])
                wrist = self.GetPointPos(shoulder, wrist_len, self.gloveData['wy'])
                hand = self.GetPointPos(wrist, hand_len, self.gloveData['hy'])

                self.handCanvas.create_line(start[0], start[1], shoulder[0], shoulder[1], width=5, fill='FireBrick')
                self.handCanvas.create_line(shoulder[0], shoulder[1], wrist[0], wrist[1], width=5, fill='ForestGreen')
                self.handCanvas.create_line(wrist[0], wrist[1], hand[0], hand[1], width=5, fill='Teal')

                self.handCanvas.create_oval(start[0] - point_size,
                                            start[1] - point_size,
                                            start[0] + point_size,
                                            start[1] + point_size,
                                            fill='SlateGray', outline='SlateGray')
                self.handCanvas.create_oval(shoulder[0] - point_size,
                                            shoulder[1] - point_size,
                                            shoulder[0] + point_size,
                                            shoulder[1] + point_size,
                                            fill='SlateGray', outline='SlateGray')
                self.handCanvas.create_oval(wrist[0] - point_size,
                                            wrist[1] - point_size,
                                            wrist[0] + point_size,
                                            wrist[1] + point_size,
                                            fill='SlateGray', outline='SlateGray')

                self.handCanvas.create_oval(self.gloveData['X'] - point_size,
                                            self.gloveData['Y'] - point_size,
                                            self.gloveData['X'] + point_size,
                                            self.gloveData['Y'] + point_size,
                                            fill='white', outline='white')

                self.handCanvas.create_arc(200-10, 107-10+5, 200+10, 107+10+5, start=90, extent=self.gloveData['sz']*3 - 90, style=ARC, outline='FireBrick', width=3)
                self.handCanvas.create_arc(200-10, 139-10+5, 200+10, 139+10+5, start=90, extent=self.gloveData['hx'], style=ARC, outline='Teal', width=3)
                self.handCanvas.create_arc(200-10, 169-10+5, 200+10, 169+10+5, start=90, extent=self.gloveData['g']*3.6, style=ARC, outline='SlateGray', width=3)

                self.handCanvas.update()
                sleep(0.1)
                self.handCanvas.delete('all')
            except UnicodeDecodeError: continue
            except: break

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
                    self.A3Label['text'] = "H:" + packet[6] + "°"
                    self.A4Label['text'] = "YAW:" + packet[1] + "°"
                    self.A5Label['text'] = "ROLL:" + packet[7] + "°"
                    self.A6Label['text'] = "GRAB:" + packet[8] + "%"

                    print(packet)

                    self.gloveData['sy'] = float(packet[0])
                    self.gloveData['sz'] = float(packet[1])

                    self.gloveData['wy'] = float(packet[2])

                    self.gloveData['X'] = float(packet[3])
                    self.gloveData['Y'] = float(packet[4])
                    self.gloveData['Z'] = float(packet[5])

                    self.gloveData['hy'] = float(packet[6])
                    self.gloveData['hx'] = float(packet[7])

                    self.gloveData['g'] = float(packet[8])

            except UnicodeDecodeError: continue
            except ValueError: continue
            except IndexError: continue

    def __init__(self):
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
            threading.Thread(target=self.getDataFromGlove).start()
            threading.Thread(target=self.DrawHand).start()
