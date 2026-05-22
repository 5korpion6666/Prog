from functools import lru_cache


# ─────────────────────────────────────────────
# Задача 1. Разделить список на n частей
# ─────────────────────────────────────────────

def split_iter(lst, n):
    """
    Итеративная версия. Разделяет список на n частей циклически.

    >>> split_iter([1,2,3,4,5], 2)
    [[1, 3, 5], [2, 4]]
    >>> split_iter([1,2,3,4,5], 3)
    [[1, 4], [2, 5], [3]]
    >>> split_iter([], 3)
    [[], [], []]
    """
    return [lst[i::n] for i in range(n)]


def split_rec(lst, n, i=0, result=None):
    """
    Рекурсивная версия. Разделяет список на n частей циклически.

    >>> split_rec([1,2,3,4,5], 2)
    [[1, 3, 5], [2, 4]]
    >>> split_rec([1,2,3,4,5], 3)
    [[1, 4], [2, 5], [3]]
    >>> split_rec([], 3)
    [[], [], []]
    """
    if result is None:
        result = [[] for _ in range(n)]
    if i >= len(lst):
        return result
    result[i % n].append(lst[i])
    return split_rec(lst, n, i + 1, result)


# ─────────────────────────────────────────────
# Задача 2. Рекуррентная последовательность
# v_i = (i+1)/(i²+1) * v_{i-1} - v_{i-2} * v_{i-3}
# v_1 = v_2 = 0, v_3 = 1.5
# ─────────────────────────────────────────────

def calc_v_iter(n):
    """
    Итеративная версия. Хранит только 3 последних значения.

    >>> calc_v_iter(1)
    0
    >>> calc_v_iter(2)
    0
    >>> calc_v_iter(3)
    1.5
    >>> abs(calc_v_iter(4) - (5/17 * 1.5)) < 1e-10
    True
    >>> abs(calc_v_iter(10) - calc_v_rec(10)) < 1e-10
    True
    """
    if n == 1 or n == 2:
        return 0
    if n == 3:
        return 1.5
    v1, v2, v3 = 0, 0, 1.5
    for k in range(4, n + 1):
        v1, v2, v3 = v2, v3, (k + 1) / (k * k + 1) * v3 - v2 * v1
    return v3


@lru_cache(maxsize=None)
def calc_v_rec(n):
    """
    Рекурсивная версия с мемоизацией через lru_cache.

    >>> calc_v_rec(1)
    0
    >>> calc_v_rec(2)
    0
    >>> calc_v_rec(3)
    1.5
    >>> abs(calc_v_rec(4) - (5/17 * 1.5)) < 1e-10
    True
    >>> abs(calc_v_rec(10) - calc_v_iter(10)) < 1e-10
    True
    """
    if n == 1 or n == 2:
        return 0
    if n == 3:
        return 1.5
    return (
        (n + 1) / (n * n + 1) * calc_v_rec(n - 1)
        - calc_v_rec(n - 2) * calc_v_rec(n - 3)
    )


# ─────────────────────────────────────────────
# Запуск
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print('Задача 1. split — итеративная:')
    print(split_iter([1, 2, 3, 4, 5], 2))
    print(split_iter([1, 2, 3, 4, 5], 3))

    print()
    print('Задача 1. split — рекурсивная:')
    print(split_rec([1, 2, 3, 4, 5], 2))
    print(split_rec([1, 2, 3, 4, 5], 3))

    print()
    print('Задача 2. v_i — итеративная:')
    for i in range(1, 11):
        print(f'  v_{i} = {calc_v_iter(i)}')

    print()
    print('Задача 2. v_i — рекурсивная:')
    for i in range(1, 11):
        print(f'  v_{i} = {calc_v_rec(i)}')
