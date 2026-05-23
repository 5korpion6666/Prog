# Лабораторная работа №6
## Генераторы

## 1. Условия задачи

### Задание (Rare + Medium)
Реализовать генератор, который обращается к внешнему API и возвращает результаты запросов. Написать тесты с помощью pytest.

### Задание (Well-done)
Реализовать многопоточную/параллельную версию генератора. Продемонстрировать повышение производительности относительно исходной версии.

---

## 2. Описание проделанной работы

1. Выбрал публичный бесплатный API курсов валют `https://open.er-api.com/v6/latest` — не требует ключа и регистрации
2. Реализовал однопоточный генератор `exchange_rates_generator(base_currencies)`:
   - Принимает список базовых валют
   - Для каждой валюты последовательно делает GET-запрос к API
   - `yield`-ает словарь с базовой валютой и курсами
   - При ошибке сети `yield`-ает словарь с ключом `error`
3. Реализовал генератор `rate_pairs_generator(pairs)`:
   - Принимает список пар валют в виде кортежей `('FROM', 'TO')`
   - Запрашивает курс для каждой пары и `yield`-ает результат
4. Реализовал многопоточный генератор `exchange_rates_generator_threaded(base_currencies, max_workers=5)`:
   - Использует `ThreadPoolExecutor` для параллельного выполнения запросов
   - `as_completed` позволяет `yield`-ать результаты по мере готовности, не дожидаясь остальных
   - Ускорение относительно однопоточной версии: **x4.1** (6.07 сек → 1.47 сек на 10 валютах)
5. Написал тесты через `pytest` с использованием `unittest.mock.patch` — реальные запросы к API не делаются

```python
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = 'https://open.er-api.com/v6/latest'


def exchange_rates_generator(base_currencies):
    for currency in base_currencies:
        try:
            response = requests.get(f'{BASE_URL}/{currency}', timeout=5)
            response.raise_for_status()
            data = response.json()
            yield {'base': data['base_code'], 'rates': data['rates']}
        except requests.exceptions.RequestException as e:
            yield {'error': str(e), 'base': currency}


def _fetch_rates(currency):
    try:
        response = requests.get(f'{BASE_URL}/{currency}', timeout=5)
        response.raise_for_status()
        data = response.json()
        return {'base': data['base_code'], 'rates': data['rates']}
    except requests.exceptions.RequestException as e:
        return {'error': str(e), 'base': currency}


def exchange_rates_generator_threaded(base_currencies, max_workers=5):
    currencies = list(base_currencies)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_fetch_rates, c): c for c in currencies}
        for future in as_completed(futures):
            yield future.result()
```

---

## 3. Скриншоты результатов

### Вывод программы и замер производительности
<img width="382" height="222" alt="лаб6_welldone" src="https://github.com/user-attachments/assets/35c10815-da7c-46af-aa0b-184be4f11ef9" />

### Тесты pytest
<img width="1175" height="286" alt="pytest6_welldone" src="https://github.com/user-attachments/assets/9da809bc-f200-411d-b1c7-29e810404a2a" />

---

## 4. Используемые материалы

1. [Генераторы в Python — документация](https://docs.python.org/3/glossary.html#term-generator)
2. [Генераторы и итераторы — Хабр](https://habr.com/ru/articles/132554/)
3. [concurrent.futures — документация Python](https://docs.python.org/3/library/concurrent.futures.html)
4. [open.er-api.com — документация API](https://www.exchangerate-api.com/docs/free)
5. [unittest.mock — документация Python](https://docs.python.org/3/library/unittest.mock.html)
6. [pytest documentation](https://docs.pytest.org/en/stable/)
