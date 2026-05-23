# lab5_rare.py

# ─────────────────────────────────────────────
# Задача 1. Замыкание для проверки диапазонов
# ─────────────────────────────────────────────

def make_range_checker(*ranges):
    """
    Замыкание, которое проверяет, находятся ли аргументы
    в допустимых диапазонах.

    Каждый элемент ranges — кортеж (min, max) для соответствующего аргумента.

    Возвращает функцию check(*args), которая:
    - возвращает True, если все аргументы в допустимых диапазонах
    - возвращает False иначе

    >>> check = make_range_checker((0, 10), (0, 100))
    >>> check(5, 50)
    True
    >>> check(5, 150)
    False
    >>> check(-1, 50)
    False
    """
    def check(*args):
        if len(args) != len(ranges):
            raise ValueError(f'Ожидается {len(ranges)} аргументов, получено {len(args)}')
        return all(lo <= arg <= hi for arg, (lo, hi) in zip(args, ranges))
    return check


# ─────────────────────────────────────────────
# Задача 2. Декоратор try/except
# ─────────────────────────────────────────────

def safe_call(func):
    """
    Декоратор, оборачивающий функцию в try/except.
    При возникновении ошибки выводит сообщение и возвращает None.

    >>> @safe_call
    ... def divide(a, b):
    ...     return a / b
    >>> divide(10, 2)
    5.0
    >>> divide(10, 0) is None  # doctest: +ELLIPSIS
    Ошибка в функции "divide": ZeroDivisionError: ...
    True
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f'Ошибка в функции "{func.__name__}": {type(e).__name__}: {e}')
            return None
    return wrapper


# ─────────────────────────────────────────────
# Применение декоратора к замыканию
# ─────────────────────────────────────────────

@safe_call
def checked_divide(a, b, lo=0, hi=100):
    """
    Пример: замыкание с проверкой диапазонов,
    обёрнутое декоратором safe_call.
    """
    check = make_range_checker((lo, hi), (lo, hi))
    if not check(a, b):
        raise ValueError(f'Аргументы {a}, {b} выходят за диапазон [{lo}, {hi}]')
    return a / b


# ─────────────────────────────────────────────
# Запуск
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print('=== Задача 1. Замыкание ===')
    check = make_range_checker((0, 10), (0, 100))
    print(f'check(5, 50)   = {check(5, 50)}')
    print(f'check(5, 150)  = {check(5, 150)}')
    print(f'check(-1, 50)  = {check(-1, 50)}')

    print()
    print('=== Задача 2. Декоратор ===')

    @safe_call
    def divide(a, b):
        return a / b

    @safe_call
    def get_item(lst, i):
        return lst[i]

    print(f'divide(10, 2)      = {divide(10, 2)}')
    print(f'divide(10, 0)      = {divide(10, 0)}')
    print(f'get_item([1,2,3], 1) = {get_item([1, 2, 3], 1)}')
    print(f'get_item([1,2,3], 9) = {get_item([1, 2, 3], 9)}')

    print()
    print('=== Декоратор применён к замыканию ===')
    print(f'checked_divide(10, 2)         = {checked_divide(10, 2)}')
    print(f'checked_divide(10, 0)         = {checked_divide(10, 0)}')
    print(f'checked_divide(200, 2)        = {checked_divide(200, 2)}')
