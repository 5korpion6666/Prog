# Лабораторная работа №6
## Генераторы

## 1. Условия задачи

Реализовать генератор, который обращается к внешнему API и возвращает результаты запросов.

---

## 2. Описание проделанной работы

1. Выбрал публичный бесплатный API курсов валют `https://open.er-api.com/v6/latest` — не требует ключа и регистрации
2. Реализовал генератор `exchange_rates_generator(base_currencies)`:
   - Принимает список базовых валют
   - Для каждой валюты делает GET-запрос к API
   - `yield`-ает словарь с базовой валютой и курсами
   - При ошибке сети `yield`-ает словарь с ключом `error` вместо исключения
3. Реализовал генератор `rate_pairs_generator(pairs)`:
   - Принимает список пар валют в виде кортежей `('FROM', 'TO')`
   - Для каждой пары запрашивает курс и `yield`-ает результат
   - Обрабатывает ошибки сети и неизвестные валюты
4. Написал тесты через `pytest` с использованием `unittest.mock.patch` — реальные запросы к API не делаются, вместо них используются моки

```python
import requests

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


def rate_pairs_generator(pairs):
    for from_currency, to_currency in pairs:
        try:
            response = requests.get(f'{BASE_URL}/{from_currency}', timeout=5)
            response.raise_for_status()
            data = response.json()
            rate = data['rates'].get(to_currency)
            if rate is None:
                yield {'error': f'Валюта {to_currency} не найдена', 'from': from_currency, 'to': to_currency}
            else:
                yield {'from': from_currency, 'to': to_currency, 'rate': rate}
        except requests.exceptions.RequestException as e:
            yield {'error': str(e), 'from': from_currency, 'to': to_currency}
```

---

## 3. Скриншоты результатов

### Вывод программы
<img width="332" height="494" alt="лаб6_rare" src="https://github.com/user-attachments/assets/bcff6528-ab35-459b-ae07-7452b39e7654" />


### Тесты pytest
<img width="1179" height="324" alt="pytest6" src="https://github.com/user-attachments/assets/31b22816-f4fb-4ae4-8d7e-678f8c5a396b" />

---

## 4. Используемые материалы

1. [Генераторы в Python — документация](https://docs.python.org/3/glossary.html#term-generator)
2. [Генераторы и итераторы — Хабр](https://habr.com/ru/articles/132554/)
3. [open.er-api.com — документация API](https://www.exchangerate-api.com/docs/free)
4. [unittest.mock — документация Python](https://docs.python.org/3/library/unittest.mock.html)
5. [pytest documentation](https://docs.pytest.org/en/stable/)
