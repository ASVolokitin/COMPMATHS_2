import math
from linecache import cache

import sympy as sp
import numpy as np
import numdifftools as nd

ABOUT_NULL = 1e-2
MAX_INTERVAL_LENGTH = 1000000

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

# def parse_two_variable_function(func_str, variables):
#     if len(variables) != 2: return None
#     x, y = sp.symbols(variables)
#     try:
#         # Парсим строку в символьное выражение
#         func = sp.sympify(func_str)
#         return func
#     except sp.SympifyError as error:
#         print(f"Ошибка: {error}")
#         return None

# TODO
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


def half_division(a, b, e, func):
    try:
        n = 0 # Счётчик итераций
        x = (a + b) / 2
        while abs(b - a) >= e:
            fx = func(x)
            if abs(fx) < e: return result_dict(x, func(x), n, "OK")

            if func(a) * fx < 0: b = x
            else: a = x
            x = (a + b) / 2
            n += 1
        return result_dict(x, func(x), n, "OK")
    except ZeroDivisionError:
        return result_dict(None, None, 0, "Ошибка при делении на 0.")


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

def deriv_half_division(a, b, e, func):
    n = 0
    x = (a + b) / 2
    while abs(b - a) >= e:
        fx = derivative(func, x)
        if abs(fx) < e: return x

        if derivative(func, a) * fx < 0: b = x
        else: a = x
        x = (a + b) / 2
        n += 1
    print(x, derivative(func, x), n)
    return derivative(func, x)

def find_derivative_max(a, b, func, samples_amount=100):
    x = a
    abs_max_value = abs(derivative(func, x))
    while x < b:
        if abs(derivative(func, x)) > abs_max_value:
            abs_max_value = abs(derivative(func, x))
        x += abs(b - a) / samples_amount
    return abs_max_value

def simple_iteration_get_phi(a, b, func_1):
    try:
        abs_der_max = find_derivative_max(a, b, func_1)
        l = 1 / abs_der_max
        if derivative(func_1, (a + b) / 2) > 0: l *= -1
        phi = lambda x : x - l * func_1(x)
        return phi
    except ZeroDivisionError:
        return None

def simple_iteration(a, b, e, func, max_iterations = 1000):
    try:
        phi = simple_iteration_get_phi(a, b, func)
        if phi is None:
            return result_dict(None, None,  0, "Ошибка при делении на 0.")
        phi_der_max_value = find_derivative_max(a, b, phi)
        if  phi_der_max_value >= 3:
            return result_dict(None, None, 0, f"Достаточное условие сходимости не выполняется. ({phi_der_max_value})")
        prev_arg = (a + b) / 2
        cur_arg = phi(prev_arg)
        n = 1
        while True:
            if abs(cur_arg - prev_arg) <= e: break
            prev_arg = cur_arg
            cur_arg = phi(cur_arg)
            n += 1
            if n > max_iterations:
                return result_dict(None, None, 0, f"Превышено допустимое количество итераций ({n}).")
            if cur_arg < a - ABOUT_NULL or cur_arg > b + ABOUT_NULL:
                prev_arg = a
                cur_arg = phi(prev_arg)
                n += 1

        return result_dict(cur_arg, func(cur_arg), n, "OK")
    except ZeroDivisionError:
        return result_dict(None, None, 0, "Ошибка при делении на 0.")

def system_simple_iteration(func_1, func_2, max_iterations = 1000):
    phi_1 = simple_iteration(func_1)


