from idlelib.configdialog import changes

import numpy as np

from util import MAX_ITERATIONS, derivative, result_dict, is_changing_sign, SAMPLES_AMOUNT, second_derivative


def get_starting_point(a, b):
    return b

def check_convergence(func, a, b):
    x_vals = np.linspace(a, b, SAMPLES_AMOUNT)
    df_x = derivative(func, x_vals[0])
    for x in x_vals[1:]:
        new_df_x = derivative(func, x)
        if new_df_x * df_x < 0: return False
        df_x = new_df_x

    x_vals = np.linspace(a, b, SAMPLES_AMOUNT)
    df_x = second_derivative(func, x_vals[0])
    for x in x_vals[1:]:
        new_df_x = second_derivative(func, x)
        if new_df_x * df_x < 0: return False
        df_x = new_df_x

    return derivative(func, a) != 0 and derivative(func, b) != 0

def new_newton(a, b, e, func):
    if not check_convergence(func, a, b):
        return result_dict(None, None, 0, "Метод не сходится по условиям сходимости")
    try:
        x = get_starting_point(a, b)
        for i in range(MAX_ITERATIONS):
            new_x = x - func(x)/derivative(func, x)
            if abs(x - new_x) <= e or abs(func(new_x)/derivative(func, new_x)) <= e or abs(func(new_x)) <= e:
                return result_dict(new_x, func(new_x), i, "OK")
            x = new_x
    except ZeroDivisionError:
        return result_dict(None, None, 0, "Ошибка при попытке деления на 0.")