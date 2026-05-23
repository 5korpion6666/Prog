# Лабораторная работа №5
## Замыкания и декораторы

## 1. Условия задач

### Задание 1
Написать замыкание, определяющее нахождение аргументов в допустимых диапазонах.

### Задание 2
Написать декоратор, который будет оборачивать каждую функцию в `try` блок для обработки ошибок. Применить декоратор к замыканию.

---

## 2. Описание проделанной работы

1. Реализовал замыкание `make_range_checker(*ranges)`:
   - Принимает произвольное количество диапазонов `(min, max)`
   - Возвращает функцию `check(*args)`, которая проверяет каждый аргумент на попадание в соответствующий диапазон
   - Диапазоны захватываются из внешней области видимости — это и есть замыкание

2. Реализовал декоратор `safe_call(func)`:
   - Оборачивает любую функцию в `try/except`
   - При ошибке выводит название функции, тип и текст ошибки
   - Возвращает `None` в случае исключения

3. Применил декоратор к замыканию в функции `checked_divide`:
   - Внутри функции создаётся замыкание `check` для проверки диапазонов аргументов
   - Вся функция обёрнута декоратором `@safe_call`

```python
from functools import lru_cache


def make_range_checker(*ranges):
    """
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


def safe_call(func):
    """
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


@safe_call
def checked_divide(a, b, lo=0, hi=100):
    check = make_range_checker((lo, hi), (lo, hi))
    if not check(a, b):
        raise ValueError(f'Аргументы {a}, {b} выходят за диапазон [{lo}, {hi}]')
    return a / b
```

---

## 3. Скриншоты результатов

<img width="659" height="323" alt="лаб5_rare" src="https://github.com/user-attachments/assets/2e3031fb-c579-44d8-8598-44f28b8aed7a" />

---

## 4. Используемые материалы

1. [Замыкания в Python — документация](https://docs.python.org/3/faq/programming.html#what-is-a-lambda-expression)
2. [Декораторы в Python — Хабр](https://habr.com/ru/articles/141411/)
3. [functools — документация Python](https://docs.python.org/3/library/functools.html)
