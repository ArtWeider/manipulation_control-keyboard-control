import telnetlib as telnet
import asyncio

class ManipulatorController:

    tn = None

    def connect(self, ip, port):
        self.tn = telnet.Telnet(ip, port, 1)

    def __init__(self):
        try:
            self.connect('192.168.137.32', '23')
        except:
            self.tn = self.FakeTn()
            print("Can't connect")

    def goToPoint(self, **kwargs):
        mess = ''
        for key in ['x', 'y', 'z', 'q']:
            if key in kwargs.keys():
                mess += f'{key.upper()}{int(kwargs[key])} '
        print(mess)
        self.tn.write(mess.encode('utf-8'))

    class FakeTn:

        def write(self, *args):
            pass
