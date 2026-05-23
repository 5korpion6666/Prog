# lab5_welldone.py

import functools
import inspect


# ─────────────────────────────────────────────
# Декоратор классов
# safe_class(cls=None, *, verbose=True)
#
# Обходит все методы класса и оборачивает каждый
# в try/except через safe_call.
# Поддерживает опциональный параметр verbose.
# Поддерживает рекурсивные методы через functools.wraps.
# ─────────────────────────────────────────────

def safe_call(func=None, *, verbose=True):
    """
    Декоратор функций: оборачивает в try/except.

    >>> @safe_call
    ... def divide(a, b):
    ...     return a / b
    >>> divide(10, 2)
    5.0
    >>> divide(10, 0) is None  # doctest: +ELLIPSIS
    Ошибка в функции "divide": ZeroDivisionError: ...
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

    if func is not None:
        return decorator(func)
    return decorator


def safe_class(cls=None, *, verbose=True):
    """
    Декоратор классов: оборачивает все публичные методы класса
    в try/except через safe_call.

    Поддерживает опциональный параметр verbose.

    >>> @safe_class
    ... class Calculator:
    ...     def divide(self, a, b):
    ...         return a / b
    >>> c = Calculator()
    >>> c.divide(10, 2)
    5.0
    >>> c.divide(10, 0) is None  # doctest: +ELLIPSIS
    Ошибка в функции "divide": ZeroDivisionError: ...
    True

    >>> @safe_class(verbose=False)
    ... class SilentCalculator:
    ...     def divide(self, a, b):
    ...         return a / b
    >>> sc = SilentCalculator()
    >>> sc.divide(10, 0) is None
    True
    """
    def decorator(cls):
        for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
            # оборачиваем только публичные методы
            if not name.startswith('__'):
                setattr(cls, name, safe_call(method, verbose=verbose))
        return cls

    if cls is not None:
        return decorator(cls)
    return decorator


# ─────────────────────────────────────────────
# Примеры использования
# ─────────────────────────────────────────────

# 1. Декоратор класса без параметров
@safe_class
class Calculator:
    def divide(self, a, b):
        return a / b

    def get_item(self, lst, i):
        return lst[i]

    def factorial(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError(f'Недопустимый аргумент: {n}')
        if n == 0:
            return 1
        return n * self.factorial(n - 1)


# 2. Декоратор класса с verbose=False
@safe_class(verbose=False)
class SilentCalculator:
    def divide(self, a, b):
        return a / b


# 3. Декоратор класса применён к классу с замыканием
def make_range_checker(*ranges):
    def check(*args):
        if len(args) != len(ranges):
            raise ValueError(f'Ожидается {len(ranges)} аргументов, получено {len(args)}')
        return all(lo <= arg <= hi for arg, (lo, hi) in zip(args, ranges))
    return check


@safe_class(verbose=True)
class RangeCalculator:
    def checked_divide(self, a, b, lo=0, hi=100):
        check = make_range_checker((lo, hi), (lo, hi))
        if not check(a, b):
            raise ValueError(f'Аргументы {a}, {b} выходят за диапазон [{lo}, {hi}]')
        return a / b


# ─────────────────────────────────────────────
# Запуск
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print('=== @safe_class без параметров ===')
    calc = Calculator()
    print(f'divide(10, 2)        = {calc.divide(10, 2)}')
    print(f'divide(10, 0)        = {calc.divide(10, 0)}')
    print(f'get_item([1,2,3], 1) = {calc.get_item([1, 2, 3], 1)}')
    print(f'get_item([1,2,3], 9) = {calc.get_item([1, 2, 3], 9)}')
    print(f'factorial(5)         = {calc.factorial(5)}')
    print(f'factorial(-1)        = {calc.factorial(-1)}')

    print()
    print('=== @safe_class(verbose=False) ===')
    silent = SilentCalculator()
    print(f'divide(10, 2)  = {silent.divide(10, 2)}')
    print(f'divide(10, 0)  = {silent.divide(10, 0)}')

    print()
    print('=== @safe_class применён к классу с замыканием ===')
    rc = RangeCalculator()
    print(f'checked_divide(10, 2)   = {rc.checked_divide(10, 2)}')
    print(f'checked_divide(10, 0)   = {rc.checked_divide(10, 0)}')
    print(f'checked_divide(200, 2)  = {rc.checked_divide(200, 2)}')
