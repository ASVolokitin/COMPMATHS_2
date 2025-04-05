import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QHBoxLayout, QLabel

from entites.equation_system import EquationSystem
from utils.calcs_util import SAMPLES_AMOUNT


class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)

        self.ax.grid(True)
        self.main_layout = QHBoxLayout()
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addLayout(layout)
        self.setLayout(self.main_layout)
        self.func_text = QLabel("")
        self.main_layout.addWidget(self.func_text)

    def plot_function(self, func, func_text, x_range):
        self.ax.clear()
        print(x_range)
        x = np.linspace(x_range[0], x_range[1], SAMPLES_AMOUNT)
        y = np.array([func(xi) for xi in x])
        self.ax.plot(x, y, label=func_text + '=0', color='darkslateblue')
        self.ax.axhline(0, color='black', linewidth=1)
        self.ax.axvline(0, color='black', linewidth=1)
        self.ax.set_xlim(x_range[0], x_range[1])
        self.ax.legend()
        self.ax.grid(True)
        self.func_text.setText("")
        self.canvas.draw()

    def plot_implicit_functions(self, selected_value : EquationSystem, x_range, y_range, start_point):
        self.ax.clear()
        x = np.linspace(x_range[0], x_range[1], SAMPLES_AMOUNT)
        y = np.linspace(y_range[0], y_range[1], SAMPLES_AMOUNT)
        X, Y = np.meshgrid(x, y)
        try:
            G = selected_value.first_func(X, Y)
            H = selected_value.second_func(X, Y)
        except ZeroDivisionError:
            print("поделил на ноль")
        self.ax.contour(X, Y, G, levels=[0], colors='orchid')
        self.ax.contour(X, Y, H, levels=[0], colors='darkslateblue')
        self.ax.axhline(0, color='black', linewidth=1)
        self.ax.axvline(0, color='black', linewidth=1)
        self.ax.scatter(start_point[0], start_point[1], color='green', s=50)
        self.ax.set_xlim(x_range[0], x_range[1])
        self.ax.set_ylim(y_range[0], y_range[1])
        if len(self.ax.get_legend_handles_labels()[0]) > 0:
            self.ax.legend()
        self.ax.grid(True)
        self.func_text.setText("f1(x, y) = " + selected_value.first_func_text + '\nf2(x, y) = ' + selected_value.second_func_text)
        self.canvas.draw()

    def add_solution_point(self, x, y):
        print(x, y, "для точки")
        self.ax.scatter(x, y, color='darkslateblue')
        self.canvas.draw()