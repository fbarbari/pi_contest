import numpy as np

from kivy.uix.boxlayout import BoxLayout

import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivy.garden.matplotlib import FigureCanvasKivy, FigureCanvasKivyAgg

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


class CircleLayout(BoxLayout):

    points = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add(self, p):
        #print("@CircleLayout.add", p)
        self.points.append(p)
        self.plot()

    def clean(self):
        self.points = []
        self.plot()

    def plot(self):

        plt.close()

        self.figure, self.ax = plt.subplots()

        self.ax.set_aspect('equal')

        self.ax.set_xlim((-1, 1))
        self.ax.set_ylim((-1, 1))

        square = plt.Rectangle((-1, -1), 2, 2, fc='w', alpha=0.0, color='w')
        circle = plt.Circle((0, 0), 1, color='r', alpha=0.5)

        self.ax.add_patch(square)
        self.ax.add_patch(circle)

        #self.ax.grid(color='black', alpha=0.2, linestyle='-', linewidth=1)

        major_ticks = np.arange(-1, 1.0001, 0.25)
        minor_ticks = np.arange(-1, 1.0001, 0.25 * 0.5)

        self.ax.set_xticks(major_ticks)
        self.ax.set_xticks(minor_ticks, minor=True)
        self.ax.set_yticks(major_ticks)
        self.ax.set_yticks(minor_ticks, minor=True)

        self.ax.grid(which='both')

        # or if you want differnet settings for the grids:
        self.ax.grid(which='minor', alpha=0.35)
        self.ax.grid(which='major', alpha=0.5)

        ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x * 100))
        self.ax.xaxis.set_major_formatter(ticks_x)

        ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x * 100))
        self.ax.yaxis.set_major_formatter(ticks_y)

        self.ax.scatter([i[0] for i in self.points], [i[1]
                                                      for i in self.points], marker='.', color='r')

        if self.points:
            self.ax.scatter(self.points[-1][0],
                            self.points[-1][1],
                            marker='.',
                            color='b')

        self.clear_widgets()
        self.add_widget(FigureCanvasKivyAgg(self.figure))
