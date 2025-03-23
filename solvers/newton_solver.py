import numpy as np
from util import result_dict, MAX_INTERVAL_LENGTH, derivative, ABOUT_NULL, check_sign_consistency, SAMPLES_AMOUNT, \
    second_derivative, df, dff, MAX_ITERATIONS

def check_convergence(func, a, b):
    x_vals = np.linspace(a, b, SAMPLES_AMOUNT)
    df_x = df(func, x_vals[0])
    for x in x_vals[1:]:
        new_df_x = df(func, x)
        if new_df_x * df_x < 0:
            return False
        df_x = new_df_x

    x_vals = np.linspace(a, b, SAMPLES_AMOUNT)
    df_x = dff(func, x_vals[0])
    for x in x_vals[1:]:
        new_df_x = dff(func, x)
        if new_df_x * df_x < 0:
            return False
        df_x = new_df_x

    return derivative(func, a) != 0 and derivative(func, b) != 0

def newton(a, b, e, func):
    if not check_convergence(func, a, b): return result_dict(None, None, 0, "Не сходится")
    try:
        x = (a + b) / 2
        n = 0
        for i in range(MAX_INTERVAL_LENGTH):
            df_x = df(func, x)
            if np.isnan(df_x) or abs(df_x) < ABOUT_NULL:
                return result_dict(None, None, 0, "Производная слишком мала или не определена в точке исследования.")
            x_new = x - func(x) / df_x
            n += 1
            if n > MAX_ITERATIONS: return result_dict(None, None,0, f"Превышено допустимое количество итераций ({n})")
            if x_new < a or x_new > b:
                x = a
                continue
            if abs(x_new - x) <= e or abs(func(x_new)/df(func, x_new)) <= e or abs(func(x_new)) <= e:
                return result_dict(x_new, func(x), n, "OK")

            x = x_new
        # if not check_sign_consistency(func, a, b) or df(func, x) < ABOUT_NULL: return result_dict(None, None, 0)
        if x < a or x > b: return result_dict(None, None, 0, "Выход за границы интервала")
        return result_dict(x, func(x), n, "OK")
    except ZeroDivisionError:
        return result_dict(None, None, 0, "Ошибка деления на 0.")
