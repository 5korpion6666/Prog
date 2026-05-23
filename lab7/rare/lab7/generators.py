# lab7/generators.py

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = 'https://open.er-api.com/v6/latest'


def exchange_rates_generator(base_currencies):
    """
    Однопоточный генератор курсов валют.

    >>> isinstance(exchange_rates_generator(['USD']), type(x for x in []))
    True
    """
    for currency in base_currencies:
        try:
            response = requests.get(f'{BASE_URL}/{currency}', timeout=5)
            response.raise_for_status()
            data = response.json()
            yield {'base': data['base_code'], 'rates': data['rates']}
        except requests.exceptions.RequestException as e:
            yield {'error': str(e), 'base': currency}


def exchange_rates_generator_threaded(base_currencies, max_workers=5):
    """
    Многопоточный генератор курсов валют.
    """
    def _fetch(currency):
        try:
            response = requests.get(f'{BASE_URL}/{currency}', timeout=5)
            response.raise_for_status()
            data = response.json()
            return {'base': data['base_code'], 'rates': data['rates']}
        except requests.exceptions.RequestException as e:
            return {'error': str(e), 'base': currency}

    currencies = list(base_currencies)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_fetch, c): c for c in currencies}
        for future in as_completed(futures):
            yield future.result()


def rate_pairs_generator(pairs):
    """
    Генератор курсов для конкретных пар валют.
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
