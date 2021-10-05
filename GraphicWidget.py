from tkinter import ttk
from config import Cfg
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def cm2inch(sm):
    return sm * 0.39

class GraphicWidget:
    X = 515 * Cfg.SIZE_MULT
    Y = 30 * Cfg.SIZE_MULT
    WIDTH = 800 * Cfg.SIZE_MULT
    HEIGHT = 700 * Cfg.SIZE_MULT

    def quit(self):
        self.root.remove()
        exit()

    class Create3DPlot:
        def __init__(self, root):
            self.figure, self.ax_3d = self.create_plot()  # Возвращает объект фигуры, нарисованной matplotlib
            self.create_form(self.figure, root)  # Отображение рисунка над формой tkinter

        def create_plot(self):
            fig = plt.figure(figsize=(cm2inch(14), cm2inch(12)))
            ax_3d = fig.add_subplot(111, projection="3d")

            return fig, ax_3d

        def create_form(self, figure, root):
            # Отображение нарисованной графики в окне tkinter
            figure.canvas.mpl_disconnect(figure.canvas.manager.key_press_handler_id)
            canvas = FigureCanvasTkAgg(figure, root)
            canvas.draw()
            canvas.get_tk_widget().place(x=GraphicWidget.X+11, y=GraphicWidget.Y+15)

    class CreatePoint:

        setPointFlag = False
        AxesSphereMovementFlag = False
        ShiftFlag = False
        CtrlFlag = False

        max = 200
        min = -200

        points = {'time': [], 'x': [], 'y': [], 'z': [], 'rad': [], 'a': [], 'b': [], 'c': []}
        params = {'x': 0, 'y': 0, 'z': 0, 'rad': 0, 'a': 0, 'b': 0, 'c': 0}

        cornerNum = 0
        selectedTime = None

        def __init__(self, root, main):
            self.main = main

            root.bind("<KeyPress>", self.place_point)
            root.bind("<KeyRelease>", self.changing_flags)

        def dictionaryUpdate(self, flag, values=(0, 0, 0, 0, 0, 0, 0, 0)):
            if flag:
                self.points['time'].append(values[0])
                self.points['x'].append(values[1])
                self.points['y'].append(values[2])
                self.points['z'].append(values[3])
                self.points['rad'].append(values[4])
                self.points['a'].append(values[5])
                self.points['b'].append(values[6])
                self.points['c'].append(values[7])
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

                for i in range(1, self.cornerNum + 1):
                    self.points['x'][-i - 1], self.points['y'][-i - 1], self.points['z'][-i - 1] = \
                        self.getSphericalCoordinates(360 / self.cornerNum * i + self.params['a'])

        def place_point(self, event):
            save = self.main.savesManager.currentSave

            # сделать линию параллельной оси координат
            if event.keysym == 'Shift_L':
                self.ShiftFlag = True
            else:
                self.ShiftFlag = False

            # удаление точек
            if event.keysym == 'Delete':
                pass  # не работет

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

                current_point = self.main.savesManager.saves[save].points[self.selectedTime]

                current_point.x = self.params['x']
                self.main.savesManager.saves[save].points[self.selectedTime].y = self.params['y']
                self.main.savesManager.saves[save].points[self.selectedTime].z = self.params['z']

                self.main.pointMenuWidget.onPointSelected(self.selectedTime)

                print(self.main.savesManager.saves[save].points[self.selectedTime].x)

    def drawObjects(self, frame):
        self.plot3d.ax_3d.clear()

        self.plot3d.ax_3d.plot3D(self.point.points['x'], self.point.points['y'], self.point.points['z'], color='orange', marker='o')
        self.plot3d.ax_3d.set_xlim(xmax=self.point.max, xmin=self.point.min)
        self.plot3d.ax_3d.set_ylim(ymax=self.point.min, ymin=self.point.max)
        self.plot3d.ax_3d.set_zlim(zmax=self.point.max + 200, zmin=self.point.min + 200)

        plt.xlabel("X")
        plt.ylabel("Y")

        if len(self.point.points['x']) > 1:

            x1 = self.point.points['x'][-1]
            x2 = self.point.points['x'][-2]

            y1 = self.point.points['y'][-1]
            y2 = self.point.points['y'][-2]

            z1 = self.point.points['z'][-1]
            z2 = self.point.points['z'][-2]

            if self.point.setPointFlag:

                if self.point.AxesSphereMovementFlag:
                    a = np.linspace(0, 360, 50)

                    x, y, z = self.point.getSphericalCoordinates(a)

                    self.plot3d.ax_3d.plot3D(x, y, z, color='gray', linestyle=':')

                if abs(z1 - z2) < 15 and abs(y1 - y2) < 15:
                    self.plot3d.ax_3d.plot3D((x1, x2), (y1, y2), (z1, z2), color='red', linestyle=':')

                    if self.point.ShiftFlag:
                        self.point.points['y'][-1] = y2
                        self.point.params['y'] = y2
                        self.point.points['z'][-1] = z2
                        self.point.params['z'] = z2

                if abs(z1 - z2) < 15 and abs(x1 - x2) < 15:
                    self.plot3d.ax_3d.plot3D((x1, x2), (y1, y2), (z1, z2), color='green', linestyle=':')

                    if self.point.ShiftFlag:
                        self.point.points['x'][-1] = x2
                        self.point.params['x'] = x2
                        self.point.points['z'][-1] = z2
                        self.point.params['z'] = z2

                if abs(x1 - x2) < 15 and abs(y1 - y2) < 15:
                    self.plot3d.ax_3d.plot3D((x1, x2), (y1, y2), (z1, z2), color='blue', linestyle=':')

                    if self.point.ShiftFlag:
                        self.point.points['x'][-1] = x2
                        self.point.params['x'] = x2
                        self.point.points['y'][-1] = y2
                        self.point.params['y'] = y2

            for i in range(len(self.point.points['x'])):
                x1 = self.point.points['x'][i - 1]
                x2 = self.point.points['x'][i]

                y1 = self.point.points['y'][i - 1]
                y2 = self.point.points['y'][i]

                z1 = self.point.points['z'][i - 1]
                z2 = self.point.points['z'][i]

                if abs(z1 - z2) == 0 and abs(y1 - y2) == 0:
                    self.plot3d.ax_3d.plot3D((x1, x2), (y1, y2), (z1, z2), color='red', marker='o')

                if abs(z1 - z2) == 0 and abs(x1 - x2) == 0:
                    self.plot3d.ax_3d.plot3D((x1, x2), (y1, y2), (z1, z2), color='green', marker='o')

                if abs(x1 - x2) == 0 and abs(y1 - y2) == 0:
                    self.plot3d.ax_3d.plot3D((x1, x2), (y1, y2), (z1, z2), color='blue', marker='o')

    def __init__(self, main):
        self.main = main
        self.root = main.root

        self.mainLabel = ttk.Frame(style="RoundedFrame", height=self.HEIGHT, width=self.WIDTH)
        self.mainLabel.place(x=self.X, y=self.Y)

        self.plot3d = self.Create3DPlot(self.root)
        self.point = self.CreatePoint(self.root, self.main)

        self.anim = animation.FuncAnimation(self.plot3d.figure, self.drawObjects, interval=100)
