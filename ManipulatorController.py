import telnetlib as telnet
import asyncio
import threading
import time
import serial.tools.list_ports
from config import Cfg as cfg

class ManipulatorController:

    main = None

    ser = None
    playThread = None

    connected = False
    paused = False

    listener = None
    listener2 = None

    toSend = ''
    completed = True

    def connect(self, name):
        self.ser = serial.Serial()
        portList = serial.tools.list_ports.comports()
        comPort = ''

        for i in range(0, len(portList)):
            port = str(portList[i])
            if name in port:
                comPort = (port.split(' ')[0])
                break
        if comPort != '':
            try:
                self.ser.port = comPort
                self.ser.baudrate = 9600
                self.ser.timeout = 1
                self.ser.open()
                self.connected = True
            except:
                self.connected = False
        else:
            self.connected = False


    def __init__(self, main):
        self.main = main
        self.connect(cfg.ManipulatorConfig.DEFAULT_NAME)

    def send(self, wait=True):
        if self.connected:
            if not wait:
                self.completed = False
                self.ser.write(self.toSend.encode('ascii'))
                print('SEND - ' + self.toSend)

    def goToPoint(self, wait=True, **kwargs):
        mess = ''
        for key in ['x', 'y', 'z', 'q']:
            if key in kwargs.keys():
                mess += f'{key.upper()}{int(kwargs[key])} '
        self.toSend = mess
        self.send(wait)

    def play(self, save):
        self.playThread = threading.Thread(target=self.playAsync, args=[save])
        self.playThread.start()

    def pause(self, status=None):
        if status == None:
            self.paused = not self.paused
        else:
            self.paused = status


    def playAsync(self, save):
        points = sorted(save.points.keys())
        pointsVar = save.points
        lastTime = 0
        for i in points:
            time.sleep(pointsVar[i].time - lastTime)
            lastTime = pointsVar[i].time
            while self.paused:
                time.sleep(0.1)
            self.goToPoint(False,
                           x=pointsVar[i].x,
                           y=pointsVar[i].y,
                           z=pointsVar[i].z,
                           q=pointsVar[i].q,
                           e=pointsVar[i].e,
                           f=pointsVar[i].f)
            self.main.xyVisualisationWidget.update(pointsVar[i].x, pointsVar[i].y)
        time.sleep(5)
        self.toSend = 'P'
        self.send(False)
        self.toSend = ''
