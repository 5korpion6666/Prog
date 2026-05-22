# Лабораторная работа №4
## Рекурсия

## 1. Условия задач

### Задание 1
Написать функцию, которая разделяет список на n частей. Элементы распределяются по подспискам циклически по индексу.

Примеры:
- `split([1,2,3,4,5], 2)` → `[[1, 3, 5], [2, 4]]`
- `split([1,2,3,4,5], 3)` → `[[1, 4], [2, 5], [3]]`

### Задание 2
Написать функцию для вычисления члена рекуррентной последовательности:

$$v_i = \frac{i+1}{i^2+1} \cdot v_{i-1} - v_{i-2} \cdot v_{i-3}$$

Начальные условия: $v_1 = 0,\ v_2 = 0,\ v_3 = 1.5$

Для каждой задачи реализовать два варианта решения: с использованием рекурсии и без рекурсии (итеративный).

---

## 2. Описание проделанной работы

1. Реализовал функцию `split_iter` — итеративное разделение списка на n частей через срезы `lst[i::n]`
2. Реализовал функцию `split_rec` — рекурсивное разделение списка с передачей индекса и аккумулятора
3. Реализовал функцию `calc_v_iter` — итеративный расчёт последовательности с хранением только трёх последних значений через tuple unpacking
4. Реализовал функцию `calc_v_rec` — рекурсивный расчёт с мемоизацией через `@lru_cache` без глобальных переменных
5. Написал тесты через `pytest` в файле `test_lab4.py` — 22 теста, все прошли
6. Повысил производительность функций минимум в 2 раза относительно исходных вариантов:
   - `split_iter`: срезы вместо двойного цикла
   - `calc_v_rec`: `@lru_cache` вместо глобального словаря
   - `calc_v_iter`: одно tuple unpacking вместо четырёх присваиваний

```python
from functools import lru_cache


def split_iter(lst, n):
    """
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


def calc_v_iter(n):
    """
    >>> calc_v_iter(1)
    0
    >>> calc_v_iter(3)
    1.5
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
    >>> calc_v_rec(1)
    0
    >>> calc_v_rec(3)
    1.5
    """
    if n == 1 or n == 2:
        return 0
    if n == 3:
        return 1.5
    return (
        (n + 1) / (n * n + 1) * calc_v_rec(n - 1)
        - calc_v_rec(n - 2) * calc_v_rec(n - 3)
    )
```

---

## 3. Скриншоты результатов

### Вывод программы
<img width="231" height="533" alt="лаб4 rare" src="https://github.com/user-attachments/assets/37d550f3-807c-456e-8b89-56fe9f39039b" />

### Тесты pytest
<img width="1184" height="476" alt="pytest4" src="https://github.com/user-attachments/assets/c5b4de78-c480-4ac0-b8d0-44dd32790bfb" />


---

## 4. Используемые материалы

1. [Recursion in Programming - Full Course - freeCodeCamp.org](https://youtu.be/IJDJ0kBx2LM)
2. [Самоучитель по Python. Часть 13: Рекурсивные функции](https://proglib.io/p/samouchitel-po-python-dlya-nachinayushchih-chast-13-rekursivnye-funkcii-2023-01-23)
3. [Как работает рекурсия – объяснение в блок-схемах и видео](https://habr.com/ru/articles/337030/)
4. [pytest documentation](https://docs.pytest.org/en/stable/)
5. [functools.lru_cache — документация Python](https://docs.python.org/3/library/functools.html#functools.lru_cache)
