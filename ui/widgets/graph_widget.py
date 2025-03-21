# import numpy as np
# import pyqtgraph as pg
#
# class GraphWidget(pg.PlotWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setBackground('w')
#         self.getAxis('left').setPen(pg.mkPen(color='k'))
#         self.getAxis('bottom').setPen(pg.mkPen(color='k'))
#         self.getAxis('left').setTextPen(pg.mkPen(color='k'))
#         self.getAxis('bottom').setTextPen(pg.mkPen(color='k'))
#         self.showGrid(x=True, y=True, alpha=0.5)
#         self.getViewBox().setBackgroundColor('w')
#
#     def plot_contour(self, X, Y, Z, level=0, color='r', label=None):
#         try:
#             import matplotlib.pyplot as plt
#             from matplotlib import cm
#             from skimage import measure
#
#             # Вычисление контурных линий уровня Z = 0
#             contours = measure.find_contours(Z, level)
#
#             for contour in contours:
#                 x_vals = X[0, 0] + contour[:, 1] * (X[0, -1] - X[0, 0]) / (X.shape[1] - 1)
#                 y_vals = Y[0, 0] + contour[:, 0] * (Y[-1, 0] - Y[0, 0]) / (Y.shape[0] - 1)
#                 self.plot(x_vals, y_vals, pen=pg.mkPen(color=color, width=2))
#
#         except Exception as e:
#             print(f"Ошибка при построении контурного графика: {e}")
#
#     def draw_graph(self, is_solving_system, single_function, single_function_text, selected_value, x_left_border,
#                    x_right_border, y_left_border=None, y_right_border=None):
#         self.clear()
#         SAMPLES_AMOUNT = 100
#
#         if not is_solving_system:
#             try:
#                 x_vals = np.linspace(x_left_border, x_right_border, SAMPLES_AMOUNT)
#                 y_vals = single_function(x_vals)
#                 self.plot(x_vals, y_vals, pen=pg.mkPen(color='b', width=2), name=single_function_text)
#                 self.setTitle(f"График функции: {single_function_text}", color='k')
#                 view_box = self.getViewBox()
#                 view_box.setLimits(
#                     xMin=x_left_border,
#                     xMax=x_right_border,
#                     yMin=min(y_vals),
#                     yMax=max(y_vals),
#                 )
#             except OverflowError:
#                 print("Ошибка вычисления: Функция принимает слишком большие значения. Измените интервал.")
#         else:
#             try:
#                 x_vals = np.linspace(x_left_border, x_right_border, SAMPLES_AMOUNT)
#                 y_vals = np.linspace(y_left_border, y_right_border, SAMPLES_AMOUNT)
#                 X, Y = np.meshgrid(x_vals, y_vals)
#
#                 Z1 = selected_value.first_func(X, Y)
#                 Z2 = selected_value.second_func(X, Y)
#
#                 self.plot_contour(X, Y, Z1, level=0, color='r', label="z1(x, y) = 0")
#                 self.plot_contour(X, Y, Z2, level=0, color='b', label="z2(x, y) = 0")
#
#                 self.setTitle("График системы уравнений")
#                 self.setLabel('bottom', 'x')
#                 self.setLabel('left', 'y')
#             except Exception as e:
#                 print(f"Ошибка построения: {e}")

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication

from util import SAMPLES_AMOUNT


class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)  # Добавляем тулбар для масштабирования

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)  # Размещаем тулбар сверху
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.ax.grid(True)  # Добавляем сетку

    def plot_function(self, func, x_range):
        """Отображает график функции f(x) = 0."""
        self.ax.clear()
        x = np.linspace(x_range[0], x_range[1], SAMPLES_AMOUNT)
        y = np.array([func(xi) for xi in x])
        self.ax.plot(x, y, label='f(x)')
        self.ax.axhline(0, color='black', linewidth=1)
        self.ax.axvline(0, color='black', linewidth=1)
        self.ax.legend()
        self.ax.grid(True)  # Добавляем сетку
        self.canvas.draw()

    def plot_implicit_functions(self, g, h, x_range, y_range):
        """Отображает графики двух функций g(x, y) = 0 и h(x, y) = 0."""
        self.ax.clear()
        x = np.linspace(x_range[0], x_range[1], SAMPLES_AMOUNT)
        y = np.linspace(y_range[0], y_range[1], SAMPLES_AMOUNT)
        X, Y = np.meshgrid(x, y)
        G = g(X, Y)
        H = h(X, Y)
        print(f"Тип g: {type(g)}, Тип h: {type(h)}")
        # self.ax.contour(X, Y, G, levels=[0], colors='r', label='g(x, y) = 0')
        self.ax.contour(X, Y, G, levels=[0], colors='r')
        # self.ax.contour(X, Y, H, levels=[0], colors='b', label='h(x, y) = 0')
        self.ax.contour(X, Y, H, levels=[0], colors='b')
        self.ax.axhline(0, color='black', linewidth=1)
        self.ax.axvline(0, color='black', linewidth=1)
        # self.ax.legend()
        self.ax.grid(True)  # Добавляем сетку
        self.canvas.draw()