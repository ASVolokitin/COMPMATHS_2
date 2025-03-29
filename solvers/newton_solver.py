from typing import Callable

import numpy as np
from utils.calcs_util import result_dict, MAX_INTERVAL_LENGTH, ABOUT_NULL, df, MAX_ITERATIONS, \
    first_derivative_chages_sign, second_derivative_chages_sign, first_derivative_becomes_null, dff


def check_convergence(func : Callable[[float], float], a : float, b : float) -> bool:
    if first_derivative_chages_sign(a, b, func) or second_derivative_chages_sign(a, b, func) or first_derivative_becomes_null(a, b, func): return False
    return df(func, a) != 0 and df(func, b) != 0 and dff(func, a) != 0 and dff(func, b) != 0

def newton(a : float, b : float, e : float, func : Callable[[float], float], dev_mode : bool) -> {}:
    if not dev_mode:
        if not check_convergence(func, a, b): return result_dict(None, None, 0, "Не сходится")
    try:
        x = b if df(func, b) * dff(func, b) > 0 else a
        for i in range(MAX_ITERATIONS):
            df_x = df(func, x)
            if np.isnan(df_x) or abs(df_x) < ABOUT_NULL:
                return result_dict(None, None, 0, "Производная слишком мала или не определена в точке исследования.")
            x_new = x - func(x) / df_x
            if x_new < a or x_new > b:
                x = a
                continue
            if abs(x_new - x) <= e or abs(func(x_new)/df(func, x_new)) <= e or abs(func(x_new)) <= e:
                return result_dict(x_new, func(x), i, "OK")

            x = x_new
        if x < a or x > b: return result_dict(None, None, 0, "Выход за границы интервала")
        return result_dict(None, None,0, f"Превышено допустимое количество итераций ({MAX_ITERATIONS})")
    except ZeroDivisionError:
        return result_dict(None, None, 0, "Ошибка деления на 0.")
