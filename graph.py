
from kivy.uix.boxlayout import BoxLayout

import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivy.garden.matplotlib import FigureCanvasKivy, FigureCanvasKivyAgg

import matplotlib.pyplot as plt
import math


class GraphLayout(BoxLayout):

    pi_values = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.plot()

    def add(self, value):
        #print("@GraphLayout.add", value)
        self.pi_values.append(value)
        self.plot()

    def clean(self):
        self.pi_values = []
        self.plot()

    def plot(self):

        try:
            value = self.pi_values[-1]
        except BaseException:
            value = 0

        title = "${0}$ = {1:10.8f}".format(r"\pi", value)
        title = "${0}$ = {1:10.8f}\n${0}$ = {2:10.8f}".format(
            r"\pi", math.pi, value)

        plt.close()

        fig, ax = plt.subplots()

        ax.axhline(y=math.pi, color='black', alpha=0.5)

        ax.set_xlabel("Number of trials", fontsize=14)
        ax.set_ylabel(r"Computed ${\pi}$ value", fontsize=14)

        ax.set_title(title, size=14)

        # if abs(value/math.pi) < 1.0:
        #    ax.set_ylim(2.5, 3.5)
        # else:
        #    ax.relim()
        #    ax.autoscale()

        ax.plot(self.pi_values, color='r')

        self.clear_widgets()
        self.add_widget(FigureCanvasKivyAgg(plt.gcf()))
