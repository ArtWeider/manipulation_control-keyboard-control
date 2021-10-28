import telnetlib as telnet
import asyncio
import threading
import time
import serial.tools.list_ports
from config import Cfg as cfg
import datetime
import time

class ManipulatorController:

    main = None

    stop = False

    gMode = False

    useHand = False

    tn = None
    playThread = None
    sendThread = None

    connected = False
    paused = False

    listener = None
    listener2 = None

    toSend = ''
    lastSend = 0

    def connect(self, name):

        try:
            self.tn = telnet.Telnet(name, '23', timeout=1)
            self.connected = True
        except:
            self.connected = False

        if self.connected:
            if True:
                self.main.controlPanelWidget.setStateAll('normal')
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
            '''except:
                pass'''



    def __init__(self, main):
        self.main = main

    def goToPoint(self, _=False, **kwargs):
        mess = self.toSend
        for key in ['x', 'y', 'z', 'q', 'e', 'f']:
            if key in kwargs.keys():
                if key == 'f':
                    if self.gMode:
                        mess += f'G{int(kwargs[key])} '
                    else:
                        mess += f'{key.upper()}{int(kwargs[key])} '
                else:
                    mess += f'{key.upper()}{int(kwargs[key])} '
        self.forceSend(mess, True)
        if self.main.pointMenuWidget.followManipulatorVar.get():
            self.main.pointMenuWidget.setStateAll('normal', True)
            self.main.pointMenuWidget.onPointToRobotPressed()
            self.main.pointMenuWidget.setStateAll('disabled', True)
        if 'x' in kwargs.keys() and 'y' in kwargs.keys():
            self.main.xyVisualisationWidget.update(x=int(kwargs['x']), y=int(kwargs['y']))
        if 'x' in kwargs.keys() and 'z' in kwargs.keys():
            self.main.xzVisualisationWidget.update(int(kwargs['x']), int(kwargs['z']))

    def play(self, save):
        self.useHand = False
        self.stop = False
        self.pause = False
        self.useHand = False
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

    def forceSend(self, data, wait=False):
        if self.connected:
            if wait:
                if (time.time() - self.lastSend) < cfg.ManipulatorConfig.SEND_LIMIT:
                    return
            toSend = data
            self.tn.write(toSend.encode('ascii'))
            self.lastSend = time.time()
            print('FORCE SEND - ' + toSend)

    def sendAsync(self):
        old_send = ''
        while True:
            time.sleep(cfg.ManipulatorConfig.SEND_LIMIT)

            try:
                if self.connected:
                    if old_send != self.toSend:
                        toSend = self.toSend
                        self.tn.write(toSend.encode('ascii'))
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
        self.useHand = True
        time.sleep(5)
        self.forceSend('P')

