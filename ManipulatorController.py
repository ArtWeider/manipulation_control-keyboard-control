import telnetlib as telnet
import asyncio
import threading
import time
import serial.tools.list_ports
from config import Cfg as cfg

class ManipulatorController:

    main = None

    stop = False

    gMode = False

    ser = None
    playThread = None
    sendThread = None

    connected = False
    paused = False

    listener = None
    listener2 = None

    toSend = ''
    lastSend = None

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

        if self.connected:
            self.main.controlPanelWidget.xEntry.delete(0, 'end')
            self.main.controlPanelWidget.yEntry.delete(0, 'end')
            self.main.controlPanelWidget.zEntry.delete(0, 'end')

            self.main.controlPanelWidget.xEntry.insert(0, int(cfg.ManipulatorConfig.START_POS['x']))
            self.main.controlPanelWidget.yEntry.insert(0, int(cfg.ManipulatorConfig.START_POS['y']))
            self.main.controlPanelWidget.zEntry.insert(0, int(cfg.ManipulatorConfig.START_POS['z']))

            self.main.controlPanelWidget.qSlider.set((float(cfg.ManipulatorConfig.START_POS['q']) / cfg.ManipulatorConfig.Q_LIMIT[1]) * 100)
            self.main.controlPanelWidget.eSlider.set((float(cfg.ManipulatorConfig.START_POS['e']) / cfg.ManipulatorConfig.E_LIMIT[1]) * 100)
            self.main.controlPanelWidget.fSlider.set((float(cfg.ManipulatorConfig.START_POS['f']) / cfg.ManipulatorConfig.F_LIMIT[1]) * 100)

            self.main.controlPanelWidget.qLabel.configure(text=f"Q: {cfg.ManipulatorConfig.START_POS['q']}")
            self.main.controlPanelWidget.eLabel.configure(text=f"E: {cfg.ManipulatorConfig.START_POS['e']}")
            self.main.controlPanelWidget.fLabel.configure(text=f"F: {cfg.ManipulatorConfig.START_POS['f']}")

            self.goToPoint(x=cfg.ManipulatorConfig.START_POS['x'],
                           y=cfg.ManipulatorConfig.START_POS['y'],
                           z=cfg.ManipulatorConfig.START_POS['z'],
                           q=cfg.ManipulatorConfig.START_POS['q'],
                           e=cfg.ManipulatorConfig.START_POS['e'],
                           f=cfg.ManipulatorConfig.START_POS['f'])



    def __init__(self, main):
        self.main = main
        self.connect(cfg.ManipulatorConfig.DEFAULT_NAME)
        self.sendThread = threading.Thread(target=self.sendAsync)
        self.sendThread.start()

    def goToPoint(self, _=False, **kwargs):
        mess = ''
        for key in ['x', 'y', 'z', 'q', 'e', 'f']:
            if key in kwargs.keys():
                if key == 'f':
                    if self.gMode:
                        mess += f'G{int(kwargs[key])} '
                    else:
                        mess += f'{key.upper()}{int(kwargs[key])} '
                else:
                    mess += f'{key.upper()}{int(kwargs[key])} '
        self.toSend = mess
        if self.main.pointMenuWidget.followManipulatorVar.get():
            self.main.pointMenuWidget.setStateAll('normal', True)
            self.main.pointMenuWidget.onPointToRobotPressed()
            self.main.pointMenuWidget.setStateAll('disabled', True)
        if 'x' in kwargs.keys() and 'y' in kwargs.keys():
            self.main.xyVisualisationWidget.update(x=int(kwargs['x']), y=int(kwargs['y']))
        if 'x' in kwargs.keys() and 'z' in kwargs.keys():
            self.main.xzVisualisationWidget.update(int(kwargs['x']), int(kwargs['z']))

    def play(self, save):
        self.stop = False
        self.playThread = threading.Thread(target=self.playAsync, args=[save])
        self.playThread.start()

    def pause(self, status=None):
        if status == None:
            self.paused = not self.paused
        else:
            self.paused = status

    def stopPlaying(self):
        self.playThread = None
        self.stop = True

    def forceSend(self, data):
        if self.connected:
            print('connecnted')
            toSend = data + '\r\n'
            print('to send')
            self.ser.write(toSend.encode('ascii'))
            print('FORCE SEND - ' + toSend)

    def sendAsync(self):
        old_send = ''
        while True:
            time.sleep(cfg.ManipulatorConfig.SEND_LIMIT)

            try:
                if self.connected:
                    if old_send != self.toSend:
                        toSend = self.toSend + '\r\n'
                        self.ser.write(toSend.encode('ascii'))
                        old_send = self.toSend
                        print('SEND - ' + toSend)
            except:
                continue

    def playAsync(self, save):
        points = sorted(save.points.keys())
        pointsVar = save.points
        lastTime = 0
        for i in points:
            if self.stop:
                self.stop = False
                return
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
        time.sleep(5)
        self.toSend = 'P'

