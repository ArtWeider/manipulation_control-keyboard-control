from math import *
import matplotlib.pyplot as plt
from rich.progress import Progress
import timeit

def square(num):
    return num**2

#def calc(Xpos, Ypos, Zpos, Qpos, L0, L1, L2, L2r, L2pr, L3, Lsrv):
def calc(**kwargs):

    L0 = kwargs["L0"]
    L1 = kwargs["L1"]
    L2 = kwargs["L2"]
    L2r = kwargs["L2r"]
    L2pr = kwargs["L2pr"]
    L3 = kwargs["L3"]
    Lsrv = kwargs["Lsrv"]
    Xp = kwargs["Xpos"]
    Yp = kwargs["Ypos"]
    Zp = kwargs["Zpos"] - L0  # скорректированная координата Z  mm
    Qp = kwargs["Qpos"]


    a0 = atan2(Yp, Xp)*57.3  # Угол поворота 0-й оси относительно выбранного вами 0 ° начала координат в плоскости XY
    # В резульате этого поворота попадаем в основную рабочую плоскость
    # Основная плоскость - в которой происходит движение звеньев L1, L2, L3.
    Xt = sqrt(square(Xp) + square(Yp))   # Координата X целевой  точки в основной плоскости движения звеньев L1, L2 и L3

    dX = L3*sin(Qp/57.3)  # Корректировка X на ориентацию 3-го звена (L3)
    dY = L3*cos(Qp/57.3)  # Корректировка Y на ориентацию 3-го звена (L3)

    Xn = Xt - dX    # Позиция X в основной плоскости, куда должен попасть шарнир 3-го звена
    Yn = Zp + dY    # Позиция Y в основной плоскости, куда должен попасть шарнир 3-го звена

    d = sqrt(square(Xn) + square(Yn))    # Длина отрезка между 1-м и 3-м  шарнирами
    q1 = atan2(Yn, Xn) * 57.3  # Вспомогательный угол 1

    sq2 = (square(d) + square(L1) - square(L2)) / (L1 * d * 2)
    q2 = acos(sq2)*57.3

    sq3 = (square(L1) + square(L2) - square(d)) / (L1 * L2 * 2)
    q3 = acos(sq3)*57.3

    a1 = 180 - (q1 + q2)   # Угол поворота сервомотора 1-й оси относительно горизонтали. 0° - сзади!!!
    a2t = 180 - q3   # Угол поворота сервомотора 2-й оси относительно 1-й
    a3 = 200 - (q2 + q3 + q1) + Qp  # Угол поворота сервы 3, где 0°  отклонен на 70° снизу от L2
    a4 = 90  # Угол поворота захвата

    Lac = sqrt(square(L1) + square(L2r) - 2 * L1 * L2r * cos(a2t/57.3))
    cAb = acos((square(L1) + square(Lac) - square(L2r)) / (2 * L1 * Lac))*57.3

    eAc = a1 - cAb
    Lce = sqrt(square(Lsrv) + square(Lac) - 2 * Lsrv * Lac * cos(eAc/57.3))

    cEa = acos((square(Lce) + square(Lsrv) - square(Lac)) / (2 * Lce * Lsrv)) * 57.3
    dEc = acos((square(Lce) + square(L2pr) - square(L1)) / (2 * Lce * L2pr)) * 57.3

    a2 = 210 - dEc - cEa  # Угол поворота сервы 2 относительно горизонтали - 30°

    return (round(a0, 1), round(a1, 1), round(a2, 1), round(a3, 1), round(a4, 1))

def calc2(**kwargs):

    L0 = kwargs["L0"]
    L1 = kwargs["L1"]
    L2 = kwargs["L2"]
    L2r = kwargs["L2r"]
    L2pr = kwargs["L2pr"]
    L3 = kwargs["L3"]
    Lsrv = kwargs["Lsrv"]
    Xp = kwargs["Xpos"]
    Yp = kwargs["Ypos"]
    Zp = kwargs["Zpos"] - L0  # скорректированная координата Z  mm
    Qp = kwargs["Qpos"]


    a0 = atan2(Yp, Xp)*57.3  # Угол поворота 0-й оси относительно выбранного вами 0 ° начала координат в плоскости XY
    # В резульате этого поворота попадаем в основную рабочую плоскость
    # Основная плоскость - в которой происходит движение звеньев L1, L2, L3.
    Xt = sqrt(square(Xp) + square(Yp))   # Координата X целевой  точки в основной плоскости движения звеньев L1, L2 и L3

    dX = L3*sin(Qp/57.3)  # Корректировка X на ориентацию 3-го звена (L3)
    dY = L3*cos(Qp/57.3)  # Корректировка Y на ориентацию 3-го звена (L3)

    Xn = Xt - dX    # Позиция X в основной плоскости, куда должен попасть шарнир 3-го звена
    Yn = Zp + dY    # Позиция Y в основной плоскости, куда должен попасть шарнир 3-го звена

    d = sqrt(square(Xn) + square(Yn))    # Длина отрезка между 1-м и 3-м  шарнирами
    q1 = atan2(Yn, Xn) * 57.3  # Вспомогательный угол 1

    sq2 = (square(d) + square(L1) - square(L2)) / (L1 * d * 2)
    q2 = acos(sq2)*57.3

    sq3 = (square(L1) + square(L2) - square(d)) / (L1 * L2 * 2)
    q3 = acos(sq3)*57.3

    a1 = 180 - (q1 + q2)   # Угол поворота сервомотора 1-й оси относительно горизонтали. 0° - сзади!!!
    a2t = 180 - q3   # Угол поворота сервомотора 2-й оси относительно 1-й
    a3 = 200 - (q2 + q3 + q1) + Qp  # Угол поворота сервы 3, где 0°  отклонен на 70° снизу от L2
    a4 = 90  # Угол поворота захвата

    Lac = sqrt(square(L1) + square(L2r) - 2 * L1 * L2r * cos(a2t/57.3))
    cAb = acos((square(L1) + square(Lac) - square(L2r)) / (2 * L1 * Lac))*57.3

    eAc = a1 - cAb
    Lce = sqrt(square(Lsrv) + square(Lac) - 2 * Lsrv * Lac * cos(eAc/57.3))

    cEa = acos((square(Lce) + square(Lsrv) - square(Lac)) / (2 * Lce * Lsrv)) * 57.3
    dEc = acos((square(Lce) + square(L2pr) - square(L1)) / (2 * Lce * L2pr)) * 57.3

    a2 = 210 - dEc - cEa  # Угол поворота сервы 2 относительно горизонтали - 30°

    return (round(a0, 1), round(a1, 1), round(a2, 1), round(a3, 1), round(a4, 1))


angles = calc(Xpos=250, Ypos=0, Zpos=1, Qpos=0, L0=290, L1=189, L2=242, L2r=91, L2pr=89, L3=120, Lsrv=20)
print(f"a0: {angles[0]}\na1: {angles[1]}\na2: {angles[2]}\na3: {angles[3]}\na4: {angles[4]}")

x_points = []
z_points = []

if (input("Graphic: " ) == ""):
    exit()

def calculatePoints():
    with Progress() as progress:
        degCalc = progress.add_task("[red]Calculating... ", total=60*300*300)
        for deg in range(0, 1):
            for z in range(0, 600, 2):
                for x in range(0, 600, 2):
                    try:
                        if not ((x < 180 and z < 350)):
                            angles = calc(Xpos=x, Ypos=0, Zpos=z, Qpos=180, L0=290, L1=189, L2=242, L2r=91, L2pr=89, L3=120, Lsrv=20)
                            if angles[1] >= 75 and angles[1] <= 179 and angles[2] >= 0 and angles[2] <= 135 and angles[3] >= 0 and angles[3] <= 240:
                                x_points.append(x)
                                z_points.append(z)
                    except:
                        pass
                    progress.update(degCalc, advance=1)


calculatePoints()

plt.scatter(x_points, z_points, s=1)
plt.scatter([0, 600], [0, 600], s=5)
plt.show()

