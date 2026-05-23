# lab7/recursion.py

from functools import lru_cache


def split_iter(lst, n):
    """
    Итеративное разделение списка на n частей.

    >>> split_iter(['USD', 'EUR', 'GBP', 'JPY'], 2)
    [['USD', 'GBP'], ['EUR', 'JPY']]
    """
    return [lst[i::n] for i in range(n)]


def split_recursive(lst, n, i=0, result=None):
    """
    Рекурсивное разделение списка на n частей.

    >>> split_recursive(['USD', 'EUR', 'GBP', 'JPY'], 2)
    [['USD', 'GBP'], ['EUR', 'JPY']]
    """
    if result is None:
        result = [[] for _ in range(n)]
    if i >= len(lst):
        return result
    result[i % n].append(lst[i])
    return split_recursive(lst, n, i + 1, result)


@lru_cache(maxsize=None)
def calc_rate_recursive(steps, initial_rate=1.0):
    """
    Рекурсивное вычисление изменения курса валюты по шагам.
    Моделирует изменение: rate_i = (i+1)/(i^2+1) * rate_{i-1}
    Начальное значение: rate_1 = initial_rate

    >>> round(calc_rate_recursive(1), 4)
    1.0
    >>> calc_rate_recursive.cache_clear()  # сброс кэша после теста
    """
    if steps <= 1:
        return initial_rate
    i = steps
    return (i + 1) / (i ** 2 + 1) * calc_rate_recursive(steps - 1, initial_rate)


def calc_rate_iterative(steps, initial_rate=1.0):
    """
    Итеративное вычисление изменения курса валюты по шагам.

    >>> round(calc_rate_iterative(1), 4)
    1.0
    >>> abs(calc_rate_iterative(5) - calc_rate_recursive(5)) < 1e-10
    True
    """
    rate = initial_rate
    for i in range(2, steps + 1):
        rate = (i + 1) / (i ** 2 + 1) * rate
    return rate
