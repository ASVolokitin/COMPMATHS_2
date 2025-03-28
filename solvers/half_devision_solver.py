from collections.abc import Callable

from utils.calcs_util import result_dict


def half_division(a : float, b : float, e : float, func : Callable[[float], float]) -> {}:
    try:
        n = 0
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