import telnetlib as telnet
import asyncio
import threading
import time

class ManipulatorController:

    tn = None
    playThread = None

    connected = False

    def connect(self, ip, port):
        self.tn = telnet.Telnet(ip, port, 1)
        self.connected = True

    def __init__(self):
        try:
            self.connect('192.168.137.198', '23')
        except:
            self.tn = self.FakeTn()
            self.connected = False
            print("Can't connect")

    def goToPoint(self, **kwargs):
        mess = ''
        for key in ['x', 'y', 'z', 'q']:
            if key in kwargs.keys():
                mess += f'{key.upper()}{int(kwargs[key])} '
        print(mess)
        self.tn.write(mess.encode('utf-8'))

    def play(self, save):
        playThreading = threading.Thread(target=self.playAsync, args=[save])
        playThreading.start()


    def playAsync(self, save):
        points = sorted(save.points.keys())
        pointsVar = save.points
        lastTime = 0
        for i in points:
            time.sleep(pointsVar[i].time - lastTime)
            lastTime = pointsVar[i].time
            self.goToPoint(x=pointsVar[i].x,
                           y=pointsVar[i].y,
                           z=pointsVar[i].z,
                           q=pointsVar[i].q,
                           e=pointsVar[i].e,
                           f=pointsVar[i].f)

    class FakeTn:

        def write(self, *args):
            pass
