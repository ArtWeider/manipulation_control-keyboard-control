import telnetlib as telnet
from math import *
import time
import random


radius = 100

tn = telnet.Telnet('192.168.137.179', '23')
print("CONNECTED")

points = []
for i in range(0, 360, 40):
    x = 200 + int(radius * cos(radians(i)))
    y = 300 + int(radius * sin(radians(i)))
    z = 300
    points.append([x, y, z])


completed = True
while True:
    for i in points:
        while not completed:
            data = tn.read_very_eager()
            if data != b'':
                print(data)
            if '#' in list(data.decode('utf-8')):
                completed = True
        completed = False
        tn.write(f'X{i[0]} Y{i[1]} Z{i[2]} Q0'.encode('utf-8'))

