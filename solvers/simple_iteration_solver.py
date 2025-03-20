from util import derivative, find_derivative_max, result_dict, ABOUT_NULL


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