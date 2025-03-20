import numpy as np
from util import result_dict, MAX_INTERVAL_LENGTH, derivative, ABOUT_NULL, check_sign_consistency

def newton(a, b, e, func, max_iter=500):
    try:
        x = (a + b) / 2
        n = 0
        for i in range(MAX_INTERVAL_LENGTH):
            df = derivative(func, x)
            if np.isnan(df) or abs(df) < ABOUT_NULL:
                return result_dict(None, None, 0, "Производная слишком мала или не определена в точке исследования.")
            x_new = x - func(x) / df
            n += 1
            if n > max_iter: return result_dict(None, None,0, f"Превышено допустимое количество итераций ({n})")
            if x_new < a or x_new > b:
                x = a
                continue
            if abs(x_new - x) <= e or abs(func(x_new)/derivative(func, x_new)) <= e or abs(func(x_new)) <= e:
                return result_dict(x_new, func(x), n, "OK")

            x = x_new
        if not check_sign_consistency(func, a, b) or derivative(func, x) < ABOUT_NULL: return result_dict(None, None, 0)
        if x < a or x > b: return result_dict(None, None, 0, "Выход за границы интервала")
        return result_dict(x, func(x), n, "OK")
    except ZeroDivisionError:
        return result_dict(None, None, 0, "Ошибка деления на 0.")
