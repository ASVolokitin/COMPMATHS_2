import sympy as sp
import numdifftools as nd

ABOUT_NULL = 1e-6
MAX_INTERVAL_LENGTH = 1000000

def derivative(f, x):
    return nd.Derivative(f)(x)

def parse_function(func_str, variable):
    x = sp.symbols(variable)
    try:
        func = sp.sympify(func_str)
        return func
    except sp.SympifyError as error:
        print(f"Ошибка: {error}")
        return None

def root_counter(a, b, func):
    n = 10000000
    root_cnt = 0
    length = ABOUT_NULL * 1000
    prev = func(a)
    cur = prev
    x = a
    print("Начинаю")
    while x <= b + ABOUT_NULL * 10000:
        cur = func(x)
        if cur == None:
            print(f"Вычисленное значение функции в точке {x} превышает допустимые ограничения на максимальный размер числа, попробуйте изменить границы исследуемого интервала.")
            return -1
        if cur * prev < 0 or (abs(cur) < ABOUT_NULL and prev >= ABOUT_NULL and (cur - prev >= ABOUT_NULL * 10000)):
            print(f"Найдена смена знака функции (x = {x})")
            root_cnt += 1
        prev = cur
        x += length
    print("Проход завершён")
    return root_cnt

def half_division(a, b, e, func):
    n = 0 # Счётчик итераций
    x = (a + b) / 2
    while abs(b - a) >= e:
        fx = func(x)
        if abs(fx) < e: return x

        if func(a) * fx < 0: b = x
        else: a = x
        x = (a + b) / 2
        n += 1

    return x

def newton(a, b, e, func):
    x = (b + a) / 2
    for i in range(MAX_INTERVAL_LENGTH):
        df = derivative(func, x)

        if abs(df) < ABOUT_NULL:
            print("Производная слишком мала, метод Ньютона не применим.")
            return None

        x_new = x - func(x) / df
        if abs(x_new - x) < e:
            return x_new

        x = x_new
    return x