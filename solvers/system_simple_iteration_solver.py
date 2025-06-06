import numpy as np
from typing import Callable
from entites.equation_system import EquationSystem
from utils.calcs_util import MAX_ITERATIONS, result_dict, SAMPLES_AMOUNT


def detect_abs_max(x_left : float, x_right : float, y_bottom : float, y_top : float, func : Callable[[float, float], float]) -> float:
    x = np.linspace(x_left, x_right, SAMPLES_AMOUNT)
    y = np.linspace(y_bottom, y_top, SAMPLES_AMOUNT)
    X, Y = np.meshgrid(x, y)
    Z = func(X, Y)
    print(np.max(np.abs(Z)))
    return np.max(np.abs(Z))

def check_convergence(x_left : float, x_right : float, y_bottom : float, y_top : float, system : EquationSystem) -> bool:
    if detect_abs_max(x_left, x_right, y_bottom, y_top, system.first_phi_dx) + detect_abs_max(x_left, x_right, y_bottom, y_top, system.first_phi_dy) < 1 * 2:
        if detect_abs_max(x_left, x_right, y_bottom, y_top, system.second_phi_dx) + detect_abs_max(x_left, x_right, y_bottom, y_top, system.second_phi_dy) < 1 * 2:
            return True
    return False

def system_simple_iteration_solver(x_left : float, x_right : float, y_bottom : float, y_top : float, x_start : float, y_start : float, accuracy : float, system : EquationSystem, dev_mode : bool) -> {}:
    if not dev_mode:
        if not check_convergence(x_left, x_right, y_bottom, y_top, system):
            return result_dict(None, None, 0, "Метод расходится.")
    try:
        n = 0
        x = x_start
        y = y_start
        print(system.name)
        while True:
            new_x = system.first_phi(x, y)
            new_y = system.second_phi(x, y)
            print(new_x, new_y)
            if any(np.isnan([new_x, new_y])) or any(np.isinf([new_x, new_y])):
                return result_dict(None, None, n, "Ошибка: вычисления привели к неопределённому значению.")
            if abs(x - new_x) < accuracy and abs(y - new_y) < accuracy:
                return result_dict(new_x, new_y, n, "OK")
            x = new_x
            y = new_y
            n += 1
            if n > MAX_ITERATIONS:
                return result_dict(None, None, n, f"Превышено допустимое количество итераций ({n}).")
    except (RuntimeWarning, OverflowError):
        return result_dict(None, None, 0, "При вычислении возникла ошибка переполнения.")