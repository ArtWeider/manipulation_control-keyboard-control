import telnetlib as telnet
import asyncio
import threading
import time

class ManipulatorController:

    main = None

    tn = None
    playThread = None

    connected = False
    paused = False

    listener = None
    listener2 = None

    toSend = ''
    completed = True

    def connect(self, ip, port):
        self.tn = telnet.Telnet(ip, port, 10)
        self.connected = True

    def __init__(self, main):
        self.main = main
        self.tn = self.FakeTn()
        self.connected = True
        self.listenerFunc()

    def listenerFunc(self):
        data = ''
        try:
            data = self.tn.read_eager().decode('utf-8')
            if data != '':
                print(data)
            if '#' in list(data):
                self.completed = True
        except:
            pass
        self.main.root.after(100, self.listenerFunc)


    def send(self, wait=True):
        if not wait or not self.completed:
            self.completed = False
            self.tn.write(self.toSend.encode('utf-8'))

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

    class FakeTn:

        def write(self, *args):
            pass

        def read_eager(self, *args):
            return b''
