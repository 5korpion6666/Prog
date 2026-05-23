# Лабораторная работа №7
## Пакеты и модули

## 1. Условие задачи

Реализовать веб-приложение на основе одного из актуальных веб-фреймворков (FastAPI, Litestar, Django).

---

## 2. Описание проделанной работы

Реализовал веб-приложение на FastAPI с 5 эндпоинтами на основе логики из пакета `lab7`:

1. **`GET /rates`** — курсы валют относительно целевой валюты, поддерживает однопоточный и многопоточный режимы
2. **`GET /pair`** — курс для конкретной пары валют
3. **`GET /benchmark`** — сравнение производительности однопоточного и многопоточного режимов
4. **`GET /split`** — разбивка списка валют на N частей (итеративно или рекурсивно)
5. **`GET /calc-rate`** — рекуррентный расчёт изменения курса по формуле из лаб 4

FastAPI автоматически генерирует интерактивную документацию Swagger по адресу `/docs`.

```python
from fastapi import FastAPI, HTTPException, Query
from lab7.generators import exchange_rates_generator, exchange_rates_generator_threaded
from lab7.recursion import split_iter, split_recursive

app = FastAPI(title='Курсы валют API')


@app.get('/rates')
def get_rates(
    currencies: str = Query('USD,EUR,GBP'),
    target: str = Query('RUB'),
    threaded: bool = Query(False),
    workers: int = Query(5, ge=1, le=20),
):
    currency_list = [c.strip().upper() for c in currencies.split(',')]
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
            results.append({'base': item['base'], 'target': target, 'rate': item['rates'].get(target)})
    return {'mode': 'threaded' if threaded else 'single', 'results': results}
```

### Запуск

```bash
py -m pip install fastapi uvicorn
py lab7_welldone.py
```

После запуска открыть в браузере:
- `http://localhost:8000/docs` — интерактивная документация Swagger
- `http://localhost:8000/rates?currencies=USD,EUR,GBP&target=RUB`
- `http://localhost:8000/pair?from_currency=USD&to_currency=RUB`
- `http://localhost:8000/benchmark?count=6`
- `http://localhost:8000/split?currencies=USD,EUR,GBP,JPY&parts=2`
- `http://localhost:8000/calc-rate?steps=10&initial=90.5`

---

## 3. Скриншоты результатов

### Swagger UI
<img width="1419" height="665" alt="Swagger UI" src="https://github.com/user-attachments/assets/91ee0ac3-0821-4541-b424-6f691d5f95d6" />

### GET /rates
<img width="1137" height="925" alt="rates_1" src="https://github.com/user-attachments/assets/132d76d1-bad4-46e9-a494-0085cf8cd169" />


<img width="1128" height="892" alt="rates_2" src="https://github.com/user-attachments/assets/612f81a2-425c-438b-9865-b6b2cd224cd7" />




### GET /pair
<img width="1134" height="862" alt="pair_1" src="https://github.com/user-attachments/assets/c25e51b8-91eb-44ca-acd7-bcb6b4f0433a" />



<img width="1129" height="500" alt="pair_2" src="https://github.com/user-attachments/assets/ebbd37b7-dafb-44d5-a153-4224cb3b20b7" />




### GET /benchmark
<img width="945" height="887" alt="bechmark" src="https://github.com/user-attachments/assets/b603484e-8b29-4ada-9bb9-fe44bed45ac7" />

---

## 4. Используемые материалы

1. [FastAPI — документация](https://fastapi.tiangolo.com/)
2. [Uvicorn — документация](https://www.uvicorn.org/)
3. [Пакеты и модули Python — документация](https://docs.python.org/3/tutorial/modules.html)
