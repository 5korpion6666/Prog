# Финансовый трекер расходов

## Описание

Веб-приложение для отслеживания личных расходов на FastAPI с хранением данных в SQLite. Предоставляет REST API для добавления, просмотра и удаления расходов, а также статистику по категориям и месяцам. Использует ту же базу данных `tracker.db`, что и GUI-версия.

---

## Инструкции по запуску

### Установка зависимостей

```bash
py -m pip install fastapi uvicorn
```

### Запуск

```bash
py tracker_web.py
```

После запуска открыть в браузере:
- `http://localhost:8000/docs` — интерактивная документация Swagger
- `http://localhost:8000/expenses` — список расходов
- `http://localhost:8000/stats` — статистика по категориям
- `http://localhost:8000/stats/monthly` — статистика по месяцам

---

## Краткая справка

### Эндпоинты

| Метод | URL | Описание |
|---|---|---|
| GET | `/expenses` | Список расходов (фильтр по категории, пагинация) |
| POST | `/expenses` | Добавить расход |
| DELETE | `/expenses/{id}` | Удалить расход по ID |
| GET | `/stats` | Статистика по категориям с долями |
| GET | `/stats/monthly` | Статистика расходов по месяцам |
| GET | `/categories` | Список доступных категорий |

### Пример запроса POST /expenses

```json
{
  "date": "25.05.2025",
  "category": "Еда",
  "amount": 250.0,
  "description": "Продукты"
}
```

### Пример ответа GET /stats

```json
{
  "total": 1500.0,
  "by_category": [
    { "category": "Еда", "total": 800.0, "count": 5, "percent": 53.3 },
    { "category": "Транспорт", "total": 700.0, "count": 3, "percent": 46.7 }
  ]
}
```

### База данных

Данные хранятся в SQLite (`tracker.db`). Структура таблицы:

```sql
CREATE TABLE expenses (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    date        TEXT    NOT NULL,
    category    TEXT    NOT NULL,
    amount      REAL    NOT NULL,
    description TEXT    DEFAULT ''
)
```

---

## Скриншоты

### Swagger UI
<img width="1412" height="666" alt="UI" src="https://github.com/user-attachments/assets/8b852dcc-5640-4c24-94a6-3cab4938782b" />

### GET /expenses
<img width="941" height="952" alt="expenses" src="https://github.com/user-attachments/assets/7c5cc90f-0f17-416c-8287-c92f7d94b458" />

### GET /stats
<img width="1416" height="616" alt="stats" src="https://github.com/user-attachments/assets/60c825ad-409c-4e8e-94da-24ec07b20fa5" />

### GET /stats/monthly
<img width="1417" height="647" alt="stats_monthly" src="https://github.com/user-attachments/assets/39233e03-27f7-4618-b88e-436ec61e038d" />

---

## Используемые материалы

1. [FastAPI — документация](https://fastapi.tiangolo.com/)
2. [Uvicorn — документация](https://www.uvicorn.org/)
3. [SQLite — документация Python](https://docs.python.org/3/library/sqlite3.html)
4. [Pydantic — документация](https://docs.pydantic.dev/)
