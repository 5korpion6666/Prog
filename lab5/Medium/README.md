# Лабораторная работа №5
## Замыкания и декораторы

## 1. Условия задач

### Задание 1 (Rare)
Написать замыкание, определяющее нахождение аргументов в допустимых диапазонах.

### Задание 2 (Rare)
Написать декоратор, который будет оборачивать каждую функцию в `try` блок для обработки ошибок. Применить декоратор к замыканию.

### Задание 3 (Medium)
Создать декоратор с опциональным параметром. Реализовать поддержку рекурсивных функций.

---

## 2. Описание проделанной работы

1. Реализовал замыкание `make_range_checker(*ranges)`:
   - Принимает произвольное количество диапазонов `(min, max)`
   - Возвращает функцию `check(*args)`, которая проверяет каждый аргумент на попадание в соответствующий диапазон
   - Диапазоны захватываются из внешней области видимости — это и есть замыкание

2. Реализовал декоратор `safe_call(func)` (Rare):
   - Оборачивает любую функцию в `try/except`
   - При ошибке выводит название функции, тип и текст ошибки
   - Возвращает `None` в случае исключения
   - Применён к замыканию в функции `checked_divide`

3. Расширил декоратор до `safe_call(func=None, *, verbose=True)` (Medium):
   - Поддерживает два способа применения: `@safe_call` и `@safe_call(verbose=False)`
   - При `verbose=False` ошибки перехватываются молча
   - Поддержка рекурсивных функций через `functools.wraps`, который сохраняет `__name__`, `__doc__` и `__wrapped__`, позволяя рекурсивным вызовам корректно находить обёртку

```python
import functools


def safe_call(func=None, *, verbose=True):
    """
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

    if func is not None:
        return decorator(func)
    return decorator


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


@safe_call(verbose=True)
def factorial(n):
    if not isinstance(n, int) or n < 0:
        raise ValueError(f'Недопустимый аргумент: {n}')
    if n == 0:
        return 1
    return n * factorial(n - 1)
```

---

## 3. Скриншоты результатов

### Rare
<img width="659" height="323" alt="лаб5_rare" src="https://github.com/user-attachments/assets/0f292b7e-4bfb-4b56-80af-28157fb37d9e" />

### Medium
<img width="670" height="374" alt="лаб5_medium" src="https://github.com/user-attachments/assets/cb263d7f-1ee4-48cc-b71b-3bc9bff01035" />

---

## 4. Используемые материалы

1. [Декораторы в Python — Хабр](https://habr.com/ru/articles/141411/)
2. [Замыкания в Python — документация](https://docs.python.org/3/faq/programming.html#what-is-a-lambda-expression)
3. [functools.wraps — документация Python](https://docs.python.org/3/library/functools.html#functools.wraps)
4. [Декораторы с параметрами — Real Python](https://realpython.com/primer-on-python-decorators/#decorators-with-arguments)
