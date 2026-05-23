# lab5_medium.py

import functools


# ─────────────────────────────────────────────
# Декоратор с опциональным параметром
# safe_call(func=None, *, verbose=True)
#
# Поддерживает два способа применения:
#   @safe_call           — без параметров
#   @safe_call(verbose=False) — с параметром
#
# Поддержка рекурсивных функций:
#   functools.wraps сохраняет __name__, __doc__ и __wrapped__,
#   что позволяет рекурсивным вызовам внутри функции
#   по-прежнему находить саму себя, а не обёртку.
# ─────────────────────────────────────────────

def safe_call(func=None, *, verbose=True):
    """
    Декоратор с опциональным параметром verbose.

    Оборачивает функцию в try/except.
    Если verbose=True (по умолчанию) — выводит сообщение об ошибке.
    Если verbose=False — молча возвращает None при ошибке.

    Поддерживает рекурсивные функции.

    Применение без параметров:
    >>> @safe_call
    ... def divide(a, b):
    ...     return a / b
    >>> divide(10, 2)
    5.0
    >>> divide(10, 0) is None  # doctest: +ELLIPSIS
    Ошибка в функции "divide": ZeroDivisionError: ...
    True

    Применение с параметром verbose=False:
    >>> @safe_call(verbose=False)
    ... def divide_silent(a, b):
    ...     return a / b
    >>> divide_silent(10, 0) is None
    True
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                if verbose:
                    print(f'Ошибка в функции "{fn.__name__}": {type(e).__name__}: {e}')
                return None
        return wrapper

    # Поддержка @safe_call без скобок
    if func is not None:
        return decorator(func)
    return decorator


# ─────────────────────────────────────────────
# Примеры использования
# ─────────────────────────────────────────────

# 1. Без параметров
@safe_call
def divide(a, b):
    return a / b


# 2. С параметром verbose=False
@safe_call(verbose=False)
def divide_silent(a, b):
    return a / b


# 3. Рекурсивная функция — факториал
@safe_call(verbose=True)
def factorial(n):
    """
    Рекурсивный факториал, обёрнутый декоратором.
    functools.wraps гарантирует, что рекурсивный вызов
    factorial(n-1) вызывает обёртку, а не голую функцию,
    поэтому ошибки на любом уровне рекурсии перехватываются.
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError(f'Недопустимый аргумент: {n}')
    if n == 0:
        return 1
    return n * factorial(n - 1)


# 4. Декоратор применён к замыканию
def make_range_checker(*ranges):
    def check(*args):
        if len(args) != len(ranges):
            raise ValueError(f'Ожидается {len(ranges)} аргументов, получено {len(args)}')
        return all(lo <= arg <= hi for arg, (lo, hi) in zip(args, ranges))
    return check


@safe_call(verbose=True)
def checked_divide(a, b, lo=0, hi=100):
    check = make_range_checker((lo, hi), (lo, hi))
    if not check(a, b):
        raise ValueError(f'Аргументы {a}, {b} выходят за диапазон [{lo}, {hi}]')
    return a / b


# ─────────────────────────────────────────────
# Запуск
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print('=== @safe_call без параметров ===')
    print(f'divide(10, 2)  = {divide(10, 2)}')
    print(f'divide(10, 0)  = {divide(10, 0)}')

    print()
    print('=== @safe_call(verbose=False) ===')
    print(f'divide_silent(10, 2)  = {divide_silent(10, 2)}')
    print(f'divide_silent(10, 0)  = {divide_silent(10, 0)}')

    print()
    print('=== Рекурсивная функция ===')
    print(f'factorial(5)   = {factorial(5)}')
    print(f'factorial(-1)  = {factorial(-1)}')
    print(f'factorial("x") = {factorial("x")}')

    print()
    print('=== Декоратор применён к замыканию ===')
    print(f'checked_divide(10, 2)   = {checked_divide(10, 2)}')
    print(f'checked_divide(10, 0)   = {checked_divide(10, 0)}')
    print(f'checked_divide(200, 2)  = {checked_divide(200, 2)}')
