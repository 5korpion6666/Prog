# lab7_welldone.py

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from typing import Optional
import time

from lab7.generators import (
    exchange_rates_generator,
    exchange_rates_generator_threaded,
    rate_pairs_generator,
)
from lab7.recursion import split_iter, split_recursive, calc_rate_iterative, calc_rate_recursive

app = FastAPI(
    title='Курсы валют API',
    description='Веб-приложение для работы с курсами валют на основе пакета lab7',
    version='1.0.0',
)

AVAILABLE_CURRENCIES = ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'CHF', 'CAD', 'AUD', 'RUB', 'KRW']


# ─────────────────────────────────────────────
# Эндпоинты
# ─────────────────────────────────────────────

@app.get('/', response_class=HTMLResponse, tags=['UI'])
def index():
    """Главная страница с документацией."""
    return """
    <html><body>
    <h1>Курсы валют API</h1>
    <p>Документация: <a href="/docs">/docs</a></p>
    <ul>
        <li><a href="/rates?currencies=USD,EUR,GBP&target=RUB">GET /rates</a> — курсы валют</li>
        <li><a href="/pair?from_currency=USD&to_currency=RUB">GET /pair</a> — пара валют</li>
        <li><a href="/benchmark?count=4">GET /benchmark</a> — сравнение производительности</li>
        <li><a href="/split?currencies=USD,EUR,GBP,JPY&parts=2">GET /split</a> — разбивка списка</li>
        <li><a href="/calc-rate?steps=10&initial=90.5">GET /calc-rate</a> — расчёт курса</li>
    </ul>
    </body></html>
    """


@app.get('/rates', tags=['Курсы валют'])
def get_rates(
    currencies: str = Query('USD,EUR,GBP', description='Валюты через запятую'),
    target: str = Query('RUB', description='Целевая валюта'),
    threaded: bool = Query(False, description='Многопоточный режим'),
    workers: int = Query(5, ge=1, le=20, description='Количество потоков'),
):
    """Получить курсы валют относительно целевой валюты."""
    currency_list = [c.strip().upper() for c in currencies.split(',')]

    for c in currency_list:
        if c not in AVAILABLE_CURRENCIES:
            raise HTTPException(status_code=400, detail=f'Неизвестная валюта: {c}')
    if len(currency_list) > 10:
        raise HTTPException(status_code=400, detail='Максимум 10 валют')

    gen = (
        exchange_rates_generator_threaded(currency_list, max_workers=workers)
        if threaded
        else exchange_rates_generator(currency_list)
    )

    results = []
    for item in gen:
        if 'error' in item:
            results.append({'base': item['base'], 'error': item['error']})
        else:
            rate = item['rates'].get(target)
            results.append({'base': item['base'], 'target': target, 'rate': rate})

    return {'mode': 'threaded' if threaded else 'single', 'results': results}


@app.get('/pair', tags=['Курсы валют'])
def get_pair(
    from_currency: str = Query('USD', description='Исходная валюта'),
    to_currency: str = Query('RUB', description='Целевая валюта'),
):
    """Получить курс для конкретной пары валют."""
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    for result in rate_pairs_generator([(from_currency, to_currency)]):
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return result


@app.get('/benchmark', tags=['Производительность'])
def get_benchmark(
    count: int = Query(6, ge=1, le=10, description='Количество валют'),
    workers: int = Query(5, ge=1, le=20, description='Количество потоков'),
):
    """Сравнить производительность однопоточного и многопоточного режимов."""
    currencies = AVAILABLE_CURRENCIES[:count]

    start = time.perf_counter()
    list(exchange_rates_generator(currencies))
    single = time.perf_counter() - start

    start = time.perf_counter()
    list(exchange_rates_generator_threaded(currencies, max_workers=workers))
    multi = time.perf_counter() - start

    return {
        'currencies_count': count,
        'single_thread_sec': round(single, 2),
        'multi_thread_sec': round(multi, 2),
        'speedup': round(single / multi, 1),
        'workers': workers,
    }


@app.get('/split', tags=['Утилиты'])
def get_split(
    currencies: str = Query('USD,EUR,GBP,JPY,CNY,RUB', description='Валюты через запятую'),
    parts: int = Query(2, ge=1, le=10, description='Количество частей'),
    recursive: bool = Query(False, description='Рекурсивная версия'),
):
    """Разбить список валют на N частей."""
    currency_list = [c.strip().upper() for c in currencies.split(',')]
    fn = split_recursive if recursive else split_iter
    result = fn(currency_list, parts)
    return {
        'mode': 'recursive' if recursive else 'iterative',
        'parts': result,
    }


@app.get('/calc-rate', tags=['Утилиты'])
def get_calc_rate(
    steps: int = Query(10, ge=1, le=100, description='Количество шагов'),
    initial: float = Query(1.0, gt=0, description='Начальный курс'),
    recursive: bool = Query(False, description='Рекурсивная версия'),
):
    """Вычислить изменение курса по рекуррентной формуле."""
    fn = calc_rate_recursive if recursive else calc_rate_iterative
    result = fn(steps, initial)
    return {
        'steps': steps,
        'initial': initial,
        'mode': 'recursive' if recursive else 'iterative',
        'result': result,
    }


# ─────────────────────────────────────────────
# Запуск
# ─────────────────────────────────────────────

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
