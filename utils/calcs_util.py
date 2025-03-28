from enum import Enum, auto

import numpy as np

from entites.equation_system import System1, System2, System3

ABOUT_NULL = 1e-6
MAX_INTERVAL_LENGTH = 1000000
MIN_INTERVAL_LENGTH = 0.5
SAMPLES_AMOUNT = 1000
MAX_ITERATIONS = 100000
MAX_DELTA = 100
dx = 0.0001

class RootCounterErrorCode(Enum):
    NO_ROOTS = -1
    DISCONTINUED_FUNCTION = -2
    MORE_THAN_ONE_ROOT = -3

system_functions_options = [System1(), System2(), System3()]

def df(func, x):

    return (func(x + dx) - func(x - dx)) / (2 * dx)

def dff(func, x):
    return (func(x + dx) - 2 * func(x) + func(x - dx)) / dx ** 2

def result_dict(root, value, iter_amout, status_msg):
    if root is None or value is None:
        root = None
        value = None
        iter_amout = 0
    return {"root": root, "value": value, "iter_amount": iter_amout, "status_msg": status_msg}

def root_counter(a, b, func):
    x_vals = np.linspace(a, b, SAMPLES_AMOUNT)
    root_cnt = 0
    prev = func(x_vals[0])
    cur = prev
    print("Обход начат")
    for x in x_vals[1:]:
        cur = func(x)
        if cur is None:
            print(f"Вычисленное значение функции в точке {x} превышает допустимые ограничения на максимальный размер числа, попробуйте изменить границы исследуемого интервала.")
            return -1
        if abs(cur - prev) > MAX_DELTA:
            print(f"Функция терпит разрыв в точке {x}")
            return RootCounterErrorCode.DISCONTINUED_FUNCTION
        if cur * prev < 0 or abs(cur) < ABOUT_NULL:
            print(f"Найдена смена знака функции (x = {x}); cur = {cur}, prev = {prev}")
            root_cnt += 1
            if root_cnt > 1:
                print("Рассекречен второй корень")
                return RootCounterErrorCode.MORE_THAN_ONE_ROOT
            if abs(cur) < ABOUT_NULL:
                print(cur)
                cur = 0
        prev = cur
    print("Обход завершён")
    return root_cnt

def derivative_abs_max(a, b, func):
    x_vals = np.linspace(a, b, SAMPLES_AMOUNT)
    return max(abs(df(func, x_vals)))

def find_func_abs_max(a, b, func):
    x_vals = np.linspace(a, b, SAMPLES_AMOUNT)
    return max(abs(func(x_vals)))

def func_chages_sign(a, b, func):
    x_vals = np.linspace(a, b, SAMPLES_AMOUNT)
    fx = func(x_vals[0])
    for x in x_vals[1:]:
        new_fx = func(x)
        if new_fx * fx < 0: return True
    return False

def first_derivative_chages_sign(a, b, func):
    x_vals = np.linspace(a, b, SAMPLES_AMOUNT)
    fx = df(func, x_vals[0])
    for x in x_vals[1:]:
        new_fx = df(func, x)
        if new_fx * fx < 0:
            print(f"Обнаружена смена знака первой производной в точке {x}.")
            return True
    return False

def second_derivative_chages_sign(a, b, func):
    x_vals = np.linspace(a, b, SAMPLES_AMOUNT)
    fx = dff(func, x_vals[0])
    for x in x_vals[1:]:
        new_fx = dff(func, x)
        if new_fx * fx < 0:
            print(f"Обнаружена смена знака второй производной в точке {x}.")
            return True
    return False

def first_derivative_becomes_null(a, b, func):
    x_vals = np.linspace(a, b, SAMPLES_AMOUNT)
    for x in x_vals:
        if df(func, x) == 0: return True
    return False