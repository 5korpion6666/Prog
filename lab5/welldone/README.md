# Лабораторная работа №5
## Замыкания и декораторы

## 1. Условия задач

### Задание 1 (Rare)
Написать замыкание, определяющее нахождение аргументов в допустимых диапазонах.

### Задание 2 (Rare)
Написать декоратор, который будет оборачивать каждую функцию в `try` блок для обработки ошибок. Применить декоратор к замыканию.

### Задание 3 (Medium)
Создать декоратор с опциональным параметром. Реализовать поддержку рекурсивных функций.

### Задание 4 (Well-done)
Реализовать декоратор классов вместо декоратора функций.

---

## 2. Описание проделанной работы

1. Реализовал замыкание `make_range_checker(*ranges)`:
   - Принимает произвольное количество диапазонов `(min, max)`
   - Возвращает функцию `check(*args)`, проверяющую каждый аргумент на попадание в диапазон
   - Диапазоны захватываются из внешней области видимости — это и есть замыкание

2. Реализовал декоратор функций `safe_call(func=None, *, verbose=True)`:
   - Оборачивает функцию в `try/except`
   - Поддерживает два способа применения: `@safe_call` и `@safe_call(verbose=False)`
   - При `verbose=False` ошибки перехватываются молча
   - Поддержка рекурсивных функций через `functools.wraps`
   - Применён к замыканию в функции `checked_divide`

3. Реализовал декоратор классов `safe_class(cls=None, *, verbose=True)`:
   - Обходит все публичные методы класса через `inspect.getmembers`
   - Применяет `safe_call` к каждому методу и записывает обёртку обратно через `setattr`
   - Поддерживает опциональный параметр `verbose`
   - Рекурсивные методы работают корректно — `self.method()` обращается к уже обёрнутой версии

```python
import functools
import inspect


def safe_call(func=None, *, verbose=True):
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
    """
    def decorator(cls):
        for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
            if not name.startswith('__'):
                setattr(cls, name, safe_call(method, verbose=verbose))
        return cls

    if cls is not None:
        return decorator(cls)
    return decorator


def make_range_checker(*ranges):
    def check(*args):
        if len(args) != len(ranges):
            raise ValueError(f'Ожидается {len(ranges)} аргументов, получено {len(args)}')
        return all(lo <= arg <= hi for arg, (lo, hi) in zip(args, ranges))
    return check


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


@safe_class(verbose=False)
class SilentCalculator:
    def divide(self, a, b):
        return a / b


@safe_class(verbose=True)
class RangeCalculator:
    def checked_divide(self, a, b, lo=0, hi=100):
        check = make_range_checker((lo, hi), (lo, hi))
        if not check(a, b):
            raise ValueError(f'Аргументы {a}, {b} выходят за диапазон [{lo}, {hi}]')
        return a / b
```

---

## 3. Скриншоты результатов

### Rare
<img width="659" height="323" alt="лаб5_rare" src="https://github.com/user-attachments/assets/02d7b9a0-8334-4df8-bfeb-93ee231d2953" />

### Medium
<img width="670" height="374" alt="лаб5_medium" src="https://github.com/user-attachments/assets/81c9be58-b254-43d1-87c4-1399d326026c" />

### Well-done
<img width="653" height="363" alt="лаб5_welldone" src="https://github.com/user-attachments/assets/7ce0b045-1779-4c36-ada9-b44166489515" />

---

## 4. Используемые материалы

1. [Декораторы в Python — Хабр](https://habr.com/ru/articles/141411/)
2. [Замыкания в Python — документация](https://docs.python.org/3/faq/programming.html#what-is-a-lambda-expression)
3. [functools.wraps — документация Python](https://docs.python.org/3/library/functools.html#functools.wraps)
4. [inspect.getmembers — документация Python](https://docs.python.org/3/library/inspect.html#inspect.getmembers)
5. [Декораторы с параметрами — Real Python](https://realpython.com/primer-on-python-decorators/#decorators-with-arguments)
