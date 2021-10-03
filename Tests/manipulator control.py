import telnetlib as telnet
from math import *
import time
import matplotlib.pyplot as plt

radius = 50

tn = telnet.Telnet('192.168.137.187', '23')
print("CONNECTED")

xp = []
yp = []

for i in range(10, 300, 20):
    x = 200 + int(radius * cos(radians(i)))
    y = 200 + int(radius * sin(radians(i)))
    xp.append(x)
    yp.append(y)

for i in enumerate(xp):

    input("...")
    print(f'X{i[1]} Y{yp[i[0]]} Z{300} Q0')
    tn.write(f'X{i[1]} Y{yp[i[0]]} Z{300} Q0'.encode('utf-8'))
