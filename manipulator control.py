import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

startX, startY, startZ = 0, 0, 0
shoulderX, shoulderY, shoulderZ = 10, 20, 30
wristX, wristY, wristZ = 20, 30, 40
handX, handY, handZ = 30, 40, 50


def cm2inch(sm):
    return sm * 0.39


class Create3DPlot:
    def __init__(self):
        self.figure, self.ax_3d = self.create_plot()  # Возвращает объект фигуры, нарисованной matplotlib
        self.create_form(self.figure)  # Отображение рисунка над формой tkinter

    def create_plot(self):
        fig = plt.figure(figsize=(cm2inch(10), cm2inch(10)), facecolor='silver', edgecolor='blue')
        ax_3d = fig.add_subplot(111, projection="3d")

        return fig, ax_3d

    def create_form(self, figure):
        # Отображение нарисованной графики в окне tkinter
        figure.canvas.mpl_disconnect(figure.canvas.manager.key_press_handler_id)
        canvas = FigureCanvasTkAgg(figure, root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, expand=1)

        canvas.tkcanvas.pack()


class CreatePoint:
    def __init__(self):
        self.setPointFlag = False
        self.AxesSphereMovementFlag = False
        self.ShiftFlag = False
        self.CtrlFlag = False

        self.max = 200
        self.min = -200

        self.points = {'x': [], 'y': [], 'z': [], 'rad': [], 'a': [], 'b': [], 'c': []}
        self.params = {'x': 0, 'y': 0, 'z': 0, 'rad': 0, 'a': 0, 'b': 0, 'c': 0}

        self.cornerNum = 0

        root.bind("<KeyPress>", self.place_point)
        root.bind("<KeyRelease>", self.changing_flags)

    def dictionaryUpdate(self, flag, values=(0, 0, 0, 0, 0, 0, 0)):
        if flag:
            self.points['x'].append(values[0])
            self.points['y'].append(values[1])
            self.points['z'].append(values[2])
            self.points['rad'].append(values[3])
            self.points['a'].append(values[4])
            self.points['b'].append(values[5])
            self.points['c'].append(values[6])
        else:
            for key in self.points.keys():
                self.points[key].pop()

    def changing_flags(self, event):
        if event.keysym == 'r':
            self.AxesSphereMovementFlag = not self.AxesSphereMovementFlag

        elif event.keysym == 'Control_L':
            self.CtrlFlag = not self.CtrlFlag

            if not self.CtrlFlag and self.setPointFlag:
                for i in range(self.cornerNum):
                    self.dictionaryUpdate(False)
                self.cornerNum = 0

        elif event.keysym == 'space':
            self.setPointFlag = not self.setPointFlag

            if self.setPointFlag:
                self.dictionaryUpdate(True, values=(self.params['x'], self.params['y'], self.params['z'], 0, 0, 0, 0))

        if not self.AxesSphereMovementFlag or not self.setPointFlag:
            self.CtrlFlag = False
            self.cornerNum = 0

    def getSphericalCoordinates(self, a):
        try:
            posX = self.points['x'][-2 - self.cornerNum]
            posY = self.points['y'][-2 - self.cornerNum]
            posZ = self.points['z'][-2 - self.cornerNum]

        except IndexError:
            posX = 0
            posY = 0
            posZ = 0

        b = self.params['b']
        c = self.params['c']

        x_ = self.params['rad'] * np.sin(np.radians(a))
        y_ = self.params['rad'] * np.cos(np.radians(a)) * np.cos(np.radians(b))

        x = x_ * np.cos(np.radians(c)) - y_ * np.sin(np.radians(c)) + posX
        y = x_ * np.sin(np.radians(c)) + y_ * np.cos(np.radians(c)) + posY

        z = self.params['rad'] * np.cos(np.radians(a)) * np.sin(np.radians(b)) + posZ

        return x, y, z

    def spherical_movement(self, event):

        # клавиши управления
        if event.keysym == 'a':
            self.params['a'] += 5
        elif event.keysym == 'd':
            self.params['a'] -= 5

        elif event.keysym == 'w':
            self.params['rad'] += 5
        elif event.keysym == 's':
            self.params['rad'] -= 5

        elif event.keysym == 'q':
            self.params['b'] += 5
        elif event.keysym == 'e':
            self.params['b'] -= 5

        elif event.keysym == 'z':
            self.params['c'] += 5
        elif event.keysym == 'c':
            self.params['c'] -= 5

        self.params['x'], self.params['y'], self.params['z'] = \
            self.getSphericalCoordinates(self.params['a'])

        self.points['rad'][-1] = self.params['rad']
        self.points['a'][-1] = self.params['a']
        self.points['b'][-1] = self.params['b']
        self.points['c'][-1] = self.params['c']

    def axes_movement(self, event):
        # клавиши управления
        if event.keysym == 'a':
            self.params['x'] += 5
        elif event.keysym == 'd':
            self.params['x'] -= 5
        elif event.keysym == 'w':
            self.params['y'] += 5
        elif event.keysym == 's':
            self.params['y'] -= 5
        elif event.keysym == 'q':
            self.params['z'] += 5
        elif event.keysym == 'e':
            self.params['z'] -= 5

            self.points['rad'][-1] = 0
            self.points['a'][-1] = 0
            self.points['b'][-1] = 0
            self.points['c'][-1] = 0

    def placing_polygon(self, event):
        if self.CtrlFlag:
            if event.keysym == 'equal' or event.keysym == 'plus':
                self.cornerNum += 1
                if self.cornerNum > 10:
                    self.cornerNum = 10
                else:
                    self.dictionaryUpdate(True)

            elif event.keysym == 'minus':

                self.cornerNum -= 1
                if self.cornerNum < 0:
                    self.cornerNum = 0
                else:
                    self.dictionaryUpdate(False)

            for i in range(1, self.cornerNum+1):
                self.points['x'][-i-1], self.points['y'][-i-1], self.points['z'][-i-1] = \
                    self.getSphericalCoordinates(360 / self.cornerNum * i + self.params['a'])


    def place_point(self, event):
        # сделать линию параллельной оси координат
        if event.keysym == 'Shift_L':
            self.ShiftFlag = True
        else:
            self.ShiftFlag = False

        # удаление точек
        if event.keysym == 'Delete':
            print()  # не работет
        # отменить размещение
        elif event.keysym == 'Escape':
            self.dictionaryUpdate(False)

            for key in self.params:
                self.params[key] = self.points[key][-1]

            self.setPointFlag = 0
            return

        if self.setPointFlag:

            # выбор типа управления
            if self.AxesSphereMovementFlag:
                self.spherical_movement(event)
                self.placing_polygon(event)
            else:
                self.axes_movement(event)

            # диапазоны
            if self.params['x'] > self.max:
                self.params['x'] = self.max
            elif self.params['x'] < self.min:
                self.params['x'] = self.min

            elif self.params['y'] > self.max:
                self.params['y'] = self.max
            elif self.params['y'] < self.min:
                self.params['y'] = self.min

            elif self.params['z'] > self.max + 200:
                self.params['z'] = self.max + 200
            elif self.params['z'] < self.min + 200:
                self.params['z'] = self.min + 200

            # присваивание координат точке
            self.points['x'][-1] = self.params['x']
            self.points['y'][-1] = self.params['y']
            self.points['z'][-1] = self.params['z']


class CreateInterface:
    def getAllList(self):
        lst = [[point.points['x']], [point.points['y']], point.points['z']]
        return lst

    def __init__(self):
        self.data_list = [('A', 'B', 'C'),
                          ('a', 'b', 'c'),
                          (1, 2, 3),
                          ('A', 'B', 'C'),
                          ('a', 'b', 'c'),
                          (1, 2, 3),
                          ('A', 'B', 'C'),
                          ('a', 'b', 'c'),
                          (1, 2, 3),
                          ('A', 'B', 'C'),
                          ('a', 'b', 'c'),
                          (1, 2, 3),
                          ('x', 'y', 'z')]

        heads = ['Name1', 'Name2', 'Name3']

        self.table = ttk.Treeview(root, show='headings')
        self.table['columns'] = heads

        for header in heads:
            self.table.heading(header, text=header, anchor='center')
            self.table.column(header, anchor='center')

        for row in self.data_list:
            self.table.insert('', tk.END, values=row)

        scrollbar = ttk.Scrollbar(root, command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.pack(expand=tk.YES, fill=tk.BOTH)


def drawObjects(frame):
    plot3d.ax_3d.clear()

    plot3d.ax_3d.plot3D(point.points['x'], point.points['y'], point.points['z'], color='orange', marker='o')
    plot3d.ax_3d.set_xlim(xmax=point.max, xmin=point.min)
    plot3d.ax_3d.set_ylim(ymax=point.min, ymin=point.max)
    plot3d.ax_3d.set_zlim(zmax=point.max + 200, zmin=point.min + 200)

    plt.xlabel("X")
    plt.ylabel("Y")

    if len(point.points['x']) > 1:

        x1 = point.points['x'][-1]
        x2 = point.points['x'][-2]

        y1 = point.points['y'][-1]
        y2 = point.points['y'][-2]

        z1 = point.points['z'][-1]
        z2 = point.points['z'][-2]

        if point.setPointFlag:

            if point.AxesSphereMovementFlag:
                a = np.linspace(0, 360, 50)

                x, y, z = point.getSphericalCoordinates(a)

                plot3d.ax_3d.plot3D(x, y, z, color='gray', linestyle=':')

            if abs(z1 - z2) < 15 and abs(y1 - y2) < 15:
                plot3d.ax_3d.plot3D((x1, x2), (y1, y2), (z1, z2), color='red', linestyle=':')

                if point.ShiftFlag:
                    point.points['y'][-1] = y2
                    point.params['y'] = y2
                    point.points['z'][-1] = z2
                    point.params['z'] = z2

            if abs(z1 - z2) < 15 and abs(x1 - x2) < 15:
                plot3d.ax_3d.plot3D((x1, x2), (y1, y2), (z1, z2), color='green', linestyle=':')

                if point.ShiftFlag:
                    point.points['x'][-1] = x2
                    point.params['x'] = x2
                    point.points['z'][-1] = z2
                    point.params['z'] = z2

            if abs(x1 - x2) < 15 and abs(y1 - y2) < 15:
                plot3d.ax_3d.plot3D((x1, x2), (y1, y2), (z1, z2), color='blue', linestyle=':')

                if point.ShiftFlag:
                    point.points['x'][-1] = x2
                    point.params['x'] = x2
                    point.points['y'][-1] = y2
                    point.params['y'] = y2

        for i in range(len(point.points['x'])):
            x1 = point.points['x'][i - 1]
            x2 = point.points['x'][i]

            y1 = point.points['y'][i - 1]
            y2 = point.points['y'][i]

            z1 = point.points['z'][i - 1]
            z2 = point.points['z'][i]

            if abs(z1 - z2) == 0 and abs(y1 - y2) == 0:
                plot3d.ax_3d.plot3D((x1, x2), (y1, y2), (z1, z2), color='red', marker='o')

            if abs(z1 - z2) == 0 and abs(x1 - x2) == 0:
                plot3d.ax_3d.plot3D((x1, x2), (y1, y2), (z1, z2), color='green', marker='o')

            if abs(x1 - x2) == 0 and abs(y1 - y2) == 0:
                plot3d.ax_3d.plot3D((x1, x2), (y1, y2), (z1, z2), color='blue', marker='o')


if __name__ == "__main__":
    root = tk.Tk()  # Создать основную форму
    root.title("Manipulator control")

    canvas = tk.Canvas(root)  # Создать холст для отображения графики

    plot3d = Create3DPlot()
    point = CreatePoint()
    interface = CreateInterface()

    anim = animation.FuncAnimation(plot3d.figure, drawObjects, interval=100)

    root.mainloop()
