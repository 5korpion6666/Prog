# lab6_welldone.py

import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = 'https://open.er-api.com/v6/latest'


# ─────────────────────────────────────────────
# Исходная версия (однопоточная)
# ─────────────────────────────────────────────

def exchange_rates_generator(base_currencies):
    """
    Однопоточный генератор курсов валют.
    Запросы выполняются последовательно один за другим.
    """
    for currency in base_currencies:
        try:
            response = requests.get(f'{BASE_URL}/{currency}', timeout=5)
            response.raise_for_status()
            data = response.json()
            yield {'base': data['base_code'], 'rates': data['rates']}
        except requests.exceptions.RequestException as e:
            yield {'error': str(e), 'base': currency}


# ─────────────────────────────────────────────
# Многопоточная версия
# ─────────────────────────────────────────────

def _fetch_rates(currency):
    """Вспомогательная функция для одного запроса."""
    try:
        response = requests.get(f'{BASE_URL}/{currency}', timeout=5)
        response.raise_for_status()
        data = response.json()
        return {'base': data['base_code'], 'rates': data['rates']}
    except requests.exceptions.RequestException as e:
        return {'error': str(e), 'base': currency}


def exchange_rates_generator_threaded(base_currencies, max_workers=5):
    """
    Многопоточный генератор курсов валют.
    Запросы выполняются параллельно через ThreadPoolExecutor.

    Параметры:
        base_currencies (iterable): список базовых валют
        max_workers (int): максимальное количество потоков

    Возвращает (yield):
        dict: {'base': str, 'rates': dict} или {'error': str, 'base': str}
    """
    currencies = list(base_currencies)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_fetch_rates, c): c for c in currencies}
        for future in as_completed(futures):
            yield future.result()


# ─────────────────────────────────────────────
# Замер производительности
# ─────────────────────────────────────────────

def benchmark(currencies):
    print(f'Тестируем на {len(currencies)} валютах...\n')

    # Однопоточная версия
    start = time.perf_counter()
    results_single = list(exchange_rates_generator(currencies))
    elapsed_single = time.perf_counter() - start
    print(f'Однопоточная версия:   {elapsed_single:.2f} сек.')

    # Многопоточная версия
    start = time.perf_counter()
    results_threaded = list(exchange_rates_generator_threaded(currencies))
    elapsed_threaded = time.perf_counter() - start
    print(f'Многопоточная версия:  {elapsed_threaded:.2f} сек.')

    speedup = elapsed_single / elapsed_threaded
    print(f'\nУскорение: x{speedup:.1f}')
    print(f'Получено результатов: {len(results_single)} / {len(results_threaded)}')

    return elapsed_single, elapsed_threaded


# ─────────────────────────────────────────────
# Запуск
# ─────────────────────────────────────────────

if __name__ == '__main__':
    currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'CHF', 'CAD', 'AUD', 'RUB', 'KRW']

    print('=== Многопоточный генератор (первые 3 результата) ===')
    for i, result in enumerate(exchange_rates_generator_threaded(currencies[:3])):
        if 'error' in result:
            print(f'  Ошибка ({result["base"]}): {result["error"]}')
        else:
            rub = result['rates'].get('RUB', 'N/A')
            print(f'  1 {result["base"]} = {rub} RUB')

    print()
    print('=== Сравнение производительности ===')
    benchmark(currencies)
