import telnetlib as telnet
from math import *
import time
import random


radius = 100

tn = telnet.Telnet('192.168.137.179', '23')
print("CONNECTED")

xp = []
yp = []

'''for i in range(0, 360, 40):
    x = 200 + int(radius * cos(radians(i)))
    y = 300 + int(radius * sin(radians(i)))
    xp.append(x)
    yp.append(y)'''

points = [[150, 150, 420], [250, 150, 420], [250, 150, 520], [150, 150, 520]]

tn.write(f'X{200} Y{200} Z{300} Q0'.encode('utf-8'))

while True:
    for i in points:
        if True:
            data = tn.read_very_eager()
            if data != b'':
                print(data)
            if '#' in list(data.decode('utf-8')):
                tn.write(f'X{i[0]} Y{i[1]} Z{i[2]} Q0'.encode('utf-8'))


i = random.randint(0, len(xp))

tn.write(f'X{xp[i]} Y{200} Z{yp[i]} Q0'.encode('utf-8'))
i = 0
while True:
    data = tn.read_very_eager()
    if data != b'':
        print(data)
    if '#' in list(data.decode('utf-8')):
        i = random.randint(0, len(xp))
        tn.write(f'X{xp[i]} Y{200} Z{yp[i]} Q0'.encode('utf-8'))



i = 0
while True:
    tn.write(f'X{xp[i]} Y{yp[i]} Z{300} Q0'.encode('utf-8'))
    print('send')
    i += 1
    while True:
        data = tn.read_very_eager()
        print(data)
        if data != b'':
            print(data)
        if '#' in list(data.decode('utf-8')):
            print('break')
            break


#tn.write(f'X{xp[i]} Y{yp[i]} Z{300} Q0'.encode('utf-8'))