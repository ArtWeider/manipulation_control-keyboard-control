import telnetlib as telnet
from math import *
import time
import random
from multiprocessing import Process

radius = 100  # радиус круга

tn = telnet.Telnet('127.0.0.1', '23')  # подключение, сюда нужный адрес вставить
print("CONNECTED")

points = []
for i in range(0, 360, 40):  # перебирает i. Аргументы: начальный угол, конечный угол, шаг
    x = 200 + int(radius * cos(radians(i)))
    y = 300 + int(radius * sin(radians(i)))  # считает x, y, и z. первые числа это смещение от манипулятора
    z = 300
    points.append([x, y, z])  # добавляет точки в список

completed = True


old_num = -5

while True:     # бесконечный цикл для повторения круга
    for i in points:    # перебирает все точки из списка
        while not completed:    # цикл, выполняющийся до тех пор, пока не придёт #
            data = tn.read_eager()  # получает имеющиеся данные
            if data != b'':     # проверяет, если ничего не отправлено, то не выводит. Нужно чтобы консоль не захламлять
                print('RECIEVE - ' + data.decode('utf-8'))
            data = data.decode('utf-8')     # переводит данные из bin в str
            if '#' in list(data):   # проверяет наличие # в данных
                num = int(data[1::])    # получает число, игнорируя первый символ в данных
                if num > old_num:   # проверяет, пришел это новый пакет, или считался старый
                    completed = True    # останавливает цикл
                    old_num = num
        completed = False   # нужно чтобы в следующий раз цикл снова начался
        tn.write(f'X{i[0]} Y{i[1]} Z{i[2]} Q0'.encode('utf-8'))     # отправляет данные на манипулятор
        print('SEND - ' + f'X{i[0]} Y{i[1]} Z{i[2]} Q0')    # координаты, отправленые на манипулятор



