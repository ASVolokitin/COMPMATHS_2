import math
from linecache import cache

import sympy as sp
import numpy as np
import numdifftools as nd

ABOUT_NULL = 1e-2
MAX_INTERVAL_LENGTH = 1000000
MIN_INTERVAL_LENGTH = 0.5
SAMPLES_AMOUNT = 10000

def derivative(f, x):
    return nd.Derivative(f)(x)

def second_derivative(f, x):
    return nd.Derivative(nd.Derivative(f))(x)

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

def find_derivative_max(a, b, func, samples_amount=100):
    x = a
    abs_max_value = abs(derivative(func, x))
    while x < b:
        if abs(derivative(func, x)) > abs_max_value:
            abs_max_value = abs(derivative(func, x))
        x += abs(b - a) / samples_amount
    return abs_max_value

# def deriv_half_division(a, b, e, func):
#     n = 0
#     x = (a + b) / 2
#     while abs(b - a) >= e:
#         fx = derivative(func, x)
#         if abs(fx) < e: return x
#
#         if derivative(func, a) * fx < 0: b = x
#         else: a = x
#         x = (a + b) / 2
#         n += 1
#     print(x, derivative(func, x), n)
#     return derivative(func, x)
#
#
# def system_simple_iteration(func_1, func_2, max_iterations = 1000):
#     phi_1 = simple_iteration(func_1)