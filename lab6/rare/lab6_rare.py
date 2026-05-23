# lab6_rare.py

import requests


# ─────────────────────────────────────────────
# Генератор, обращающийся к API курсов валют
# API: https://open.er-api.com/v6/latest
# Бесплатный, без ключа
# ─────────────────────────────────────────────

BASE_URL = 'https://open.er-api.com/v6/latest'


def exchange_rates_generator(base_currencies):
    """
    Генератор, который последовательно запрашивает курсы валют
    для каждой базовой валюты из списка.

    Параметры:
        base_currencies (iterable): список базовых валют, например ['USD', 'EUR', 'RUB']

    Возвращает (yield):
        dict: {'base': str, 'rates': dict} или {'error': str, 'base': str}
    """
    for currency in base_currencies:
        try:
            response = requests.get(f'{BASE_URL}/{currency}', timeout=5)
            response.raise_for_status()
            data = response.json()
            yield {'base': data['base_code'], 'rates': data['rates']}
        except requests.exceptions.RequestException as e:
            yield {'error': str(e), 'base': currency}


def rate_pairs_generator(pairs):
    """
    Генератор, который возвращает курс для конкретных пар валют.

    Параметры:
        pairs (iterable): список кортежей ('FROM', 'TO'), например [('USD', 'EUR')]

    Возвращает (yield):
        dict: {'from': str, 'to': str, 'rate': float} или {'error': str}
    """
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


# ─────────────────────────────────────────────
# Запуск
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print('=== Курсы валют относительно USD, EUR, GBP ===')
    target = ['RUB', 'EUR', 'GBP', 'JPY', 'CNY']
    for result in exchange_rates_generator(['USD', 'EUR', 'GBP']):
        if 'error' in result:
            print(f'  Ошибка ({result["base"]}): {result["error"]}')
        else:
            print(f'\n  Базовая валюта: {result["base"]}')
            for currency in target:
                rate = result['rates'].get(currency, 'N/A')
                print(f'    1 {result["base"]} = {rate} {currency}')

    print()
    print('=== Конкретные пары валют ===')
    pairs = [('USD', 'RUB'), ('EUR', 'RUB'), ('GBP', 'RUB'), ('USD', 'EUR'), ('USD', 'CNY')]
    for result in rate_pairs_generator(pairs):
        if 'error' in result:
            print(f'  Ошибка: {result["error"]}')
        else:
            print(f'  1 {result["from"]} = {result["rate"]} {result["to"]}')
