import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk  # NavigationToolbar2TkAgg
from time import sleep

xs = []
ys = []
zs = []

setPointFlag = 0
ShiftFlag = False
CtrlFlag = False

startX, startY, startZ = 0, 0, 0
shoulderX, shoulderY, shoulderZ = 10, 20, 30
wristX, wristY, wristZ = 20, 30, 40
handX, handY, handZ = 30, 40, 50


def cm2inch(sm):
    return sm * 0.39

def createPoint(event):
    global setPointFlag
    eventType = int(event.type)

    x, y, z = 0, 0, 20

    if eventType == 5: setPointFlag += 1
    if setPointFlag > 1:
        setPointFlag = 0

    if eventType == 5 and setPointFlag:
        xs.append(x)
        ys.append(y)
        zs.append(z)

    if eventType == 6 and setPointFlag:
        xs[-1] = event.y
        zs[-1] = -event.x

        print(xs, ys)


class Form:
    def __init__(self):
        self.figure, self.ax_3d = self.create_plot()  # Возвращает объект фигуры, нарисованной matplotlib
        self.create_form(self.figure)  # Отображение рисунка над формой tkinter

    def create_plot(self):
        fig = plt.figure(figsize=(cm2inch(15), cm2inch(10)), facecolor='silver', edgecolor='blue')
        ax_3d = fig.add_subplot(projection="3d")

        return fig, ax_3d

    def create_form(self, figure):
        # Отображение нарисованной графики в окне tkinter
        canvas = FigureCanvasTkAgg(figure, root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, expand=1)


if __name__ == "__main__":
    root = tk.Tk()  # Создать основную форму
    root.title("Manipulator control")

    canvas = tk.Canvas()  # Создать холст для отображения графики

    tk.Button(root, text='Enter').pack()

    form = Form()


    def drawObjects(i):
        form.ax_3d.clear()
        plt.xlim(xmax=200, xmin=0)
        plt.ylim(ymax=0, ymin=200)

        form.ax_3d.plot3D(xs, zs, ys, color='orange', marker='o')


    ani = animation.FuncAnimation(form.figure, drawObjects, interval=100)

    root.bind("<ButtonRelease-1>", createPoint)
    root.bind("<Motion>", createPoint)

    root.mainloop()