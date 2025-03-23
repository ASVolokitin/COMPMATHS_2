import math
from linecache import cache

import sympy as sp
import numpy as np
import numdifftools as nd

from entites.equation_system import System1, System2, System3

ABOUT_NULL = 1e-2
MAX_INTERVAL_LENGTH = 1000000
MIN_INTERVAL_LENGTH = 0.5
SAMPLES_AMOUNT = 1000
MAX_ITERATIONS = 100000

system_functions_options = [System1(), System2(), System3()]

def derivative(f, x):
    return nd.Derivative(f)(x)

def second_derivative(f, x):
    return nd.Derivative(nd.Derivative(f))(x)

def df(func, x):
    dx = 0.0001
    return (func(x + dx) - func(x - dx)) / (2 * dx)

def dff(func, x):
    dx = 0.0001
    return (func(x + dx) - 2 * func(x) + func(x - dx)) / dx ** 2

def result_dict(root, value, iter_amout, status_msg):
    if root is None or value is None:
        root = None
        value = None
        iter_amout = 0
    return {"root": root, "value": value, "iter_amount": iter_amout, "status_msg": status_msg}

def parse_single_function(func_str, variable):
    x = sp.symbols(variable)
    try:
        func = sp.sympify(func_str)
        return func
    except sp.SympifyError as error:
        print(f"Ошибка: {error}")
        return None

def parse_multi_variable_function(func_str, variables):
    syms = sp.symbols(variables)
    try:
        func = sp.sympify(func_str)
        return func
    except sp.SympifyError as error:
        print(f"Ошибка: {error}")
        return None

def root_counter(a, b, func):
    n = 1000000
    root_cnt = 0
    length = ABOUT_NULL * 100
    prev = func(a)
    cur = prev
    x = a
    print("Обход начат")
    while x <= b + ABOUT_NULL:
        cur = func(x)
        if cur == None:
            print(f"Вычисленное значение функции в точке {x} превышает допустимые ограничения на максимальный размер числа, попробуйте изменить границы исследуемого интервала.")
            return -1
        # if cur * prev < 0 or (abs(cur) < ABOUT_NULL and prev >= ABOUT_NULL and (cur - prev >= ABOUT_NULL * 10000)):
        if cur * prev < 0 or abs(cur) < ABOUT_NULL:
            print(f"Найдена смена знака функции (x = {x})")
            root_cnt += 1
            if cur * prev < 0: print(prev, cur)
            if abs(cur) < ABOUT_NULL:
                print(cur)
                cur = 0
        prev = cur
        x += length
    print("Обход завершён")
    print(root_cnt)
    return root_cnt

def check_sign_consistency(func, a, b, num_points=100):
    x_vals = np.linspace(a, b, num_points)
    first_deriv_sign = np.sign(derivative(func, x_vals[0]))
    second_deriv_sign = np.sign(second_derivative(func, x_vals[0]))

    for x in x_vals[1:]:
        d1 = np.sign(derivative(func, x))
        d2 = np.sign(second_derivative(func, x))

        if d1 != first_deriv_sign or d2 != second_deriv_sign:
            return False
    return True

def is_changing_sign(func, a, b):
    x_vals = np.linspace(a, b, SAMPLES_AMOUNT)
    s = func(x_vals[0])
    for x in x_vals[1:]:
        new_s = func(x)
        if new_s * s < 0: return True
        s = new_s
    return False

def find_derivative_max(a, b, func, samples_amount=100):
    x = a
    abs_max_value = abs(derivative(func, x))
    while x < b:
        if abs(derivative(func, x)) > abs_max_value:
            abs_max_value = abs(derivative(func, x))
        x += abs(b - a) / samples_amount
    return abs_max_value

def partial_derivative(f_lambda, variables, diff_var, point):
    f_sympy = f_lambda(*variables)
    df_dvar = sp.diff(f_sympy, diff_var)
    df_dvar_lambda = sp.lambdify(variables, df_dvar, 'numpy')
    return df_dvar_lambda(*point)

# # Определяем переменные
# x, y = sp.symbols('x y')
#
# # Пример лямбда-функции
# f_lambda = lambda x, y: x ** 2 + 3 * x * y + y ** 2
#
# # Вычисляем ∂f/∂x в точке (1, 2)
# result = partial_derivative(f_lambda, (x, y), x, (1, 2))
# print("∂f/∂x в точке (1,2):", result)


def load_stylesheet(filename):
    """Загружает стили из CSS-файла."""
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()