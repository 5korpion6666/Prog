# main.py

import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
import time

from lab7.generators import (
    exchange_rates_generator,
    exchange_rates_generator_threaded,
    rate_pairs_generator,
)
from lab7.decorators import CurrencyValidator
from lab7.recursion import split_iter, split_recursive, calc_rate_iterative, calc_rate_recursive

app = typer.Typer(help='Утилита для работы с курсами валют')
console = Console()
validator = CurrencyValidator()

AVAILABLE_CURRENCIES = ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'CHF', 'CAD', 'AUD', 'RUB', 'KRW']


@app.command()
def rates(
    currencies: str = typer.Option(
        'USD,EUR,GBP',
        '--currencies', '-c',
        help='Список валют через запятую (например: USD,EUR,GBP)'
    ),
    target: str = typer.Option(
        'RUB',
        '--target', '-t',
        help='Целевая валюта для отображения курса'
    ),
    threaded: bool = typer.Option(
        False,
        '--threaded',
        help='Использовать многопоточный режим'
    ),
    workers: int = typer.Option(
        5,
        '--workers', '-w',
        help='Количество потоков (только для --threaded)'
    ),
):
    """Получить курсы валют относительно целевой валюты."""
    currency_list = [c.strip().upper() for c in currencies.split(',')]

    for c in currency_list:
        validator.validate_currency(c)
    validator.validate_count(len(currency_list))
    if threaded:
        validator.validate_workers(workers)

    gen = (
        exchange_rates_generator_threaded(currency_list, max_workers=workers)
        if threaded
        else exchange_rates_generator(currency_list)
    )

    mode = f'многопоточный ({workers} потоков)' if threaded else 'однопоточный'
    console.print(f'\n[bold]Режим:[/bold] {mode}')

    table = Table(title=f'Курсы валют → {target}')
    table.add_column('Базовая валюта', style='cyan')
    table.add_column(f'1 BASE = ? {target}', style='green')

    for result in gen:
        if 'error' in result:
            console.print(f'[red]Ошибка ({result["base"]}): {result["error"]}[/red]')
        else:
            rate = result['rates'].get(target, 'N/A')
            table.add_row(result['base'], str(rate))

    console.print(table)


@app.command()
def pair(
    from_currency: str = typer.Argument(..., help='Исходная валюта (например: USD)'),
    to_currency: str = typer.Argument(..., help='Целевая валюта (например: RUB)'),
):
    """Получить курс для конкретной пары валют."""
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    for result in rate_pairs_generator([(from_currency, to_currency)]):
        if 'error' in result:
            console.print(f'[red]Ошибка: {result["error"]}[/red]')
        else:
            console.print(f'\n[bold]1 {result["from"]} = {result["rate"]} {result["to"]}[/bold]')


@app.command()
def benchmark(
    count: int = typer.Option(
        6,
        '--count', '-n',
        help='Количество валют для теста (1-10)'
    ),
    workers: int = typer.Option(
        5,
        '--workers', '-w',
        help='Количество потоков'
    ),
):
    """Сравнить производительность однопоточного и многопоточного режимов."""
    validator.validate_count(count)
    validator.validate_workers(workers)

    currencies = AVAILABLE_CURRENCIES[:count]
    console.print(f'\n[bold]Тест производительности на {count} валютах[/bold]')

    start = time.perf_counter()
    list(exchange_rates_generator(currencies))
    single = time.perf_counter() - start

    start = time.perf_counter()
    list(exchange_rates_generator_threaded(currencies, max_workers=workers))
    multi = time.perf_counter() - start

    table = Table(title='Результаты')
    table.add_column('Режим', style='cyan')
    table.add_column('Время (сек)', style='green')
    table.add_row('Однопоточный', f'{single:.2f}')
    table.add_row(f'Многопоточный ({workers} потоков)', f'{multi:.2f}')
    table.add_row('Ускорение', f'x{single/multi:.1f}')

    console.print(table)


@app.command()
def split(
    currencies: str = typer.Option(
        'USD,EUR,GBP,JPY,CNY,RUB',
        '--currencies', '-c',
        help='Список валют через запятую'
    ),
    parts: int = typer.Option(
        2,
        '--parts', '-p',
        help='На сколько частей разбить список'
    ),
    recursive: bool = typer.Option(
        False,
        '--recursive',
        help='Использовать рекурсивную версию'
    ),
):
    """Разбить список валют на N частей."""
    currency_list = [c.strip().upper() for c in currencies.split(',')]
    fn = split_recursive if recursive else split_iter
    mode = 'рекурсивная' if recursive else 'итеративная'

    result = fn(currency_list, parts)
    console.print(f'\n[bold]Режим:[/bold] {mode}')

    table = Table(title=f'Список разбит на {parts} части')
    for i, chunk in enumerate(result):
        table.add_column(f'Часть {i + 1}', style='cyan')

    table.add_row(*[', '.join(chunk) for chunk in result])
    console.print(table)


@app.command()
def calc_rate(
    steps: int = typer.Argument(..., help='Количество шагов'),
    initial: float = typer.Option(1.0, '--initial', '-i', help='Начальный курс'),
    recursive: bool = typer.Option(False, '--recursive', help='Рекурсивная версия'),
):
    """Вычислить изменение курса по рекуррентной формуле."""
    fn = calc_rate_recursive if recursive else calc_rate_iterative
    mode = 'рекурсивная' if recursive else 'итеративная'
    result = fn(steps, initial)
    console.print(f'\n[bold]Режим:[/bold] {mode}')
    console.print(f'[bold]Результат после {steps} шагов:[/bold] {result:.6f}')


if __name__ == '__main__':
    app()
