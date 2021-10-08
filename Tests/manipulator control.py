import telnetlib as telnet
from math import *
import time


radius = 100

tn = telnet.Telnet('192.168.137.198', '23')
print("CONNECTED")

xp = []
yp = []

for i in range(0, 360, 10):
    x = 200 + int(radius * cos(radians(i)))
    y = 200 + int(radius * sin(radians(i)))
    xp.append(x)
    yp.append(y)

for i in enumerate(xp):
    tn.read_until(b'#')
    print(f'X{i[1]} Y{yp[i[0]]} Z{300} Q0')
    tn.write(f'X{i[1]} Y{yp[i[0]]} Z{300} Q0'.encode('utf-8'))
