from collections.abc import Callable

import numpy as np

from utils.calcs_util import derivative_abs_max, result_dict, ABOUT_NULL, MAX_ITERATIONS, df, SAMPLES_AMOUNT


def check_convergence(a : float, b : float, phi : Callable[[float], float]) -> bool:
    for x in np.linspace(a, b, SAMPLES_AMOUNT):
        if df(phi, x) is None: return False
    if derivative_abs_max(a, b, phi) < 1 * 3: return True
    return False

def simple_iteration_get_phi(a : float, b : float, func : Callable[[float], float]) -> Callable[[float], float]:
    try:
        abs_der_max = derivative_abs_max(a, b, func)
        l = 1 / abs_der_max
        if df(func, (a + b) / 2) > 0: l *= -1
        phi = lambda x : x - l * func(x)
        return phi
    except ZeroDivisionError:
        return None

def simple_iteration(a : float, b : float, e : float, func : Callable[[float], float], dev_mode : bool) -> {}:
    try:
        phi = simple_iteration_get_phi(a, b, func)
        if phi is None:
            return result_dict(None, None,  0, "Ошибка при делении на 0.")
        if not dev_mode:
            if not check_convergence(a, b, phi): return result_dict(None, None, 0, f"Достаточное условие сходимости не выполняется.")
        prev_arg = (a + b) / 2
        cur_arg = phi(prev_arg)
        n = 1
        while True:
            if abs(cur_arg - prev_arg) <= e: break
            prev_arg = cur_arg
            cur_arg = phi(cur_arg)
            n += 1
            if n > MAX_ITERATIONS:
                return result_dict(None, None, 0, f"Превышено допустимое количество итераций ({n}).")
            if cur_arg < a - ABOUT_NULL or cur_arg > b + ABOUT_NULL:
                prev_arg = a
                cur_arg = phi(prev_arg)
                n += 1

        return result_dict(cur_arg, func(cur_arg), n, "OK") if abs(func(cur_arg)) < ABOUT_NULL else result_dict(None, None, 0, "Не сходится")
    except ZeroDivisionError:
        return result_dict(None, None, 0, "Ошибка при делении на 0.")