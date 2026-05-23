# Лабораторная работа №7
## Пакеты и модули

## 1. Условия задачи

### Задание (Rare)
Создать пакет, содержащий 3 модуля на основе лабораторных работ №№ 4-6. Написать запускающий модуль на основе Typer, который позволит выбирать и настраивать параметры запуска логики из пакета.

---

## 2. Описание проделанной работы

### Структура пакета

```
lab7/
├── __init__.py       — инициализация пакета
├── generators.py     — генераторы курсов валют (лаб 6)
├── decorators.py     — декораторы и замыкания (лаб 5)
└── recursion.py      — рекурсия и split (лаб 4)
main.py               — Typer CLI
```

### Модули

1. **`generators.py`** — однопоточный и многопоточный генераторы курсов валют, генератор пар валют. Использует `requests` и `concurrent.futures.ThreadPoolExecutor`

2. **`decorators.py`** — декоратор `safe_call` с опциональным параметром `verbose`, декоратор классов `safe_class`, замыкание `make_range_checker`. Класс `CurrencyValidator` с валидацией параметров, обёрнутый `@safe_class`

3. **`recursion.py`** — итеративный и рекурсивный `split`, итеративный и рекурсивный расчёт изменения курса по рекуррентной формуле с мемоизацией через `@lru_cache`

4. **`main.py`** — CLI на Typer с 5 командами:
   - `rates` — курсы валют с выбором режима (однопоточный/многопоточный)
   - `pair` — курс для конкретной пары валют
   - `benchmark` — сравнение производительности режимов
   - `split` — разбивка списка валют на части
   - `calc-rate` — рекуррентный расчёт изменения курса

```python
# Пример использования CLI
py main.py rates --currencies USD,EUR,GBP --target RUB
py main.py rates --currencies USD,EUR,GBP,JPY,CNY --threaded --workers 5
py main.py pair USD RUB
py main.py benchmark --count 6
py main.py split --currencies USD,EUR,GBP,JPY,CNY,RUB --parts 3
py main.py calc-rate 10 --initial 90.5
```

---

## 3. Скриншоты результатов

### `rates`
<img width="499" height="192" alt="лаб7_rates" src="https://github.com/user-attachments/assets/b2836080-e238-4093-a705-4e0fac2baaa0" />

### `pair`
<img width="276" height="60" alt="лаб7_pair" src="https://github.com/user-attachments/assets/e16c4992-d731-4606-9a78-eb373010d1ed" />

### `benchmark`
<img width="327" height="185" alt="лаб7_benchmark" src="https://github.com/user-attachments/assets/2c65b124-992a-4a76-b613-47f2cb06391f" />

### `split`
<img width="560" height="150" alt="лаб7_split" src="https://github.com/user-attachments/assets/bdec3103-549b-4363-92ba-195c975699e8" />

### `calc-rate`
<img width="386" height="74" alt="лаб7_calc-rate" src="https://github.com/user-attachments/assets/055a3dbb-677a-452c-a96b-efacbecc1f26" />
---

## 4. Используемые материалы

1. [Typer — документация](https://typer.tiangolo.com/)
2. [Rich — документация](https://rich.readthedocs.io/en/stable/)
3. [Пакеты и модули Python — документация](https://docs.python.org/3/tutorial/modules.html)
4. [concurrent.futures — документация Python](https://docs.python.org/3/library/concurrent.futures.html)
5. [requests — документация](https://requests.readthedocs.io/en/latest/)
