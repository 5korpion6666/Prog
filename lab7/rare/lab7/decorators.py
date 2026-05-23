# lab7/decorators.py

import functools
import inspect


def safe_call(func=None, *, verbose=True):
    """
    Декоратор функций: оборачивает в try/except.
    Поддерживает опциональный параметр verbose.
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
    Декоратор классов: оборачивает все публичные методы в try/except.
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
    """
    Замыкание: проверяет аргументы на попадание в диапазоны.

    >>> check = make_range_checker((0, 100))
    >>> check(50)
    True
    >>> check(150)
    False
    """
    def check(*args):
        if len(args) != len(ranges):
            raise ValueError(f'Ожидается {len(ranges)} аргументов, получено {len(args)}')
        return all(lo <= arg <= hi for arg, (lo, hi) in zip(args, ranges))
    return check


@safe_class(verbose=True)
class CurrencyValidator:
    """
    Класс для валидации параметров запросов к API курсов валют.
    Декоратор safe_class оборачивает все методы в try/except.
    """

    VALID_CURRENCIES = {
        'USD', 'EUR', 'GBP', 'JPY', 'CNY',
        'CHF', 'CAD', 'AUD', 'RUB', 'KRW'
    }

    def validate_currency(self, currency):
        """Проверяет, является ли валюта допустимой."""
        if currency not in self.VALID_CURRENCIES:
            raise ValueError(f'Неизвестная валюта: {currency}')
        return True

    def validate_count(self, count):
        """Проверяет количество запрашиваемых валют (1-10)."""
        check = make_range_checker((1, 10))
        if not check(count):
            raise ValueError(f'Количество валют должно быть от 1 до 10, получено {count}')
        return True

    def validate_workers(self, workers):
        """Проверяет количество потоков (1-20)."""
        check = make_range_checker((1, 20))
        if not check(workers):
            raise ValueError(f'Количество потоков должно быть от 1 до 20, получено {workers}')
        return True
