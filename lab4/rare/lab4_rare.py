# lab4_rare.py
# ─────────────────────────────────────────────
# Задача 1. Разделить список на n частей
# ─────────────────────────────────────────────

def split(lst, n):
    """
    Итеративная версия.
    Разделяет список на n частей, распределяя элементы по индексу.

    >>> split([1,2,3,4,5], 2)
    [[1, 3, 5], [2, 4]]
    >>> split([1,2,3,4,5], 3)
    [[1, 4], [2, 5], [3]]
    >>> split([], 3)
    [[], [], []]
    """
    result = [[] for _ in range(n)]
    for i, x in enumerate(lst):
        result[i % n].append(x)
    return result


def split_recursive(lst, n, result=None, i=0):
    """
    Рекурсивная версия.
    Разделяет список на n частей, распределяя элементы по индексу.

    >>> split_recursive([1,2,3,4,5], 2)
    [[1, 3, 5], [2, 4]]
    >>> split_recursive([1,2,3,4,5], 3)
    [[1, 4], [2, 5], [3]]
    >>> split_recursive([], 3)
    [[], [], []]
    """
    if result is None:
        result = [[] for _ in range(n)]
    if i == len(lst):
        return result
    result[i % n].append(lst[i])
    return split_recursive(lst, n, result, i + 1)


# ─────────────────────────────────────────────
# Задача 2. Вычислить v_i по формуле
# v_i = (i+1)/(i²+1) * v_{i-1} - v_{i-2} * v_{i-3}
# v_1 = v_2 = 0, v_3 = 1.5
# ─────────────────────────────────────────────

def v_iter(n):
    """
    Итеративная версия.
    Вычисляет v_n по формуле:
    v_i = (i+1)/(i^2+1) * v_{i-1} - v_{i-2} * v_{i-3}
    Начальные условия: v_1 = v_2 = 0, v_3 = 1.5

    >>> v_iter(1)
    0
    >>> v_iter(2)
    0
    >>> v_iter(3)
    1.5
    >>> abs(v_iter(4) - (5/17 * 1.5)) < 1e-10
    True
    """
    if n == 1:
        return 0
    if n == 2:
        return 0
    if n == 3:
        return 1.5
    v = [0, 0, 1.5]
    for i in range(4, n + 1):
        vi = (i + 1) / (i**2 + 1) * v[-1] - v[-2] * v[-3]
        v.append(vi)
        v.pop(0)
    return v[-1]


def v_recursive(n, memo=None):
    """
    Рекурсивная версия с мемоизацией.
    Вычисляет v_n по формуле:
    v_i = (i+1)/(i^2+1) * v_{i-1} - v_{i-2} * v_{i-3}
    Начальные условия: v_1 = v_2 = 0, v_3 = 1.5

    >>> v_recursive(1)
    0
    >>> v_recursive(2)
    0
    >>> v_recursive(3)
    1.5
    >>> abs(v_recursive(4) - v_iter(4)) < 1e-10
    True
    >>> abs(v_recursive(10) - v_iter(10)) < 1e-10
    True
    """
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n == 1:
        return 0
    if n == 2:
        return 0
    if n == 3:
        return 1.5
    result = (
        (n + 1) / (n**2 + 1) * v_recursive(n - 1, memo)
        - v_recursive(n - 2, memo) * v_recursive(n - 3, memo)
    )
    memo[n] = result
    return result


# ─────────────────────────────────────────────
# Запуск
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print('Задача 1. split — итеративная:')
    print(split([1, 2, 3, 4, 5], 2))
    print(split([1, 2, 3, 4, 5], 3))

    print()
    print('Задача 1. split — рекурсивная:')
    print(split_recursive([1, 2, 3, 4, 5], 2))
    print(split_recursive([1, 2, 3, 4, 5], 3))

    print()
    print('Задача 2. v_i — итеративная:')
    for i in range(1, 11):
        print(f'  v_{i} = {v_iter(i)}')

    print()
    print('Задача 2. v_i — рекурсивная:')
    for i in range(1, 11):
        print(f'  v_{i} = {v_recursive(i)}')
