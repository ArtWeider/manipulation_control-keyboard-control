import telnetlib as telnet
from math import *
import time
import random


radius = 100

tn = telnet.Telnet('127.0.0.1', '23')
print("CONNECTED")

points = []
for i in range(0, 360, 40):
    x = 200 + int(radius * cos(radians(i)))
    y = 300 + int(radius * sin(radians(i)))
    z = 300
    points.append([x, y, z])

old_num = -5
completed = True
while True:
    for i in points:
        while not completed:
            data = tn.read_eager()
            if data != b'':
                print(data)
            data = data.decode('utf-8')
            if '#' in list(data):
                num = int(data[1::])
                if num > old_num:
                    completed = True
                    old_num = num
        completed = False
        tn.write(f'X{i[0]} Y{i[1]} Z{i[2]} Q0'.encode('utf-8'))

