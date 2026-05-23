# tracker_web.py — Финансовый трекер расходов (Well-done — FastAPI)

import sqlite3
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

DB_PATH = 'tracker.db'
CATEGORIES = ['Еда', 'Транспорт', 'Жильё', 'Развлечения', 'Здоровье', 'Одежда', 'Прочее']

app = FastAPI(
    title='Финансовый трекер',
    description='Веб-приложение для отслеживания расходов',
    version='1.0.0',
)


# ─────────────────────────────────────────────
# БД
# ─────────────────────────────────────────────

def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                date        TEXT    NOT NULL,
                category    TEXT    NOT NULL,
                amount      REAL    NOT NULL,
                description TEXT    DEFAULT ''
            )
        ''')
        conn.commit()


init_db()


# ─────────────────────────────────────────────
# Схемы
# ─────────────────────────────────────────────

class ExpenseCreate(BaseModel):
    date: str = Field(..., example='25.05.2025', description='Дата в формате dd.MM.yyyy')
    category: str = Field(..., example='Еда')
    amount: float = Field(..., gt=0, example=250.0)
    description: Optional[str] = Field('', example='Продукты')


class ExpenseResponse(BaseModel):
    id: int
    date: str
    category: str
    amount: float
    description: str


# ─────────────────────────────────────────────
# Эндпоинты
# ─────────────────────────────────────────────

@app.get('/', response_class=HTMLResponse, tags=['UI'])
def index():
    """Главная страница."""
    return """
    <html><body>
    <h1>Финансовый трекер</h1>
    <p>Документация: <a href="/docs">/docs</a></p>
    <ul>
        <li><b>GET</b>  <a href="/expenses">/expenses</a> — список расходов</li>
        <li><b>POST</b> /expenses — добавить расход</li>
        <li><b>DELETE</b> /expenses/{id} — удалить расход</li>
        <li><b>GET</b>  <a href="/stats">/stats</a> — статистика по категориям</li>
        <li><b>GET</b>  <a href="/stats/monthly">/stats/monthly</a> — статистика по месяцам</li>
        <li><b>GET</b>  <a href="/categories">/categories</a> — список категорий</li>
    </ul>
    </body></html>
    """


@app.get('/categories', tags=['Справочники'])
def get_categories():
    """Получить список доступных категорий."""
    return {'categories': CATEGORIES}


@app.get('/expenses', response_model=list[ExpenseResponse], tags=['Расходы'])
def get_expenses(
    category: Optional[str] = Query(None, description='Фильтр по категории'),
    limit: int = Query(100, ge=1, le=1000, description='Количество записей'),
    offset: int = Query(0, ge=0, description='Смещение'),
):
    """Получить список расходов с фильтрацией и пагинацией."""
    with get_connection() as conn:
        if category:
            if category not in CATEGORIES:
                raise HTTPException(status_code=400, detail=f'Неизвестная категория: {category}')
            rows = conn.execute(
                'SELECT id, date, category, amount, description FROM expenses WHERE category=? ORDER BY id DESC LIMIT ? OFFSET ?',
                (category, limit, offset)
            ).fetchall()
        else:
            rows = conn.execute(
                'SELECT id, date, category, amount, description FROM expenses ORDER BY id DESC LIMIT ? OFFSET ?',
                (limit, offset)
            ).fetchall()
    return [
        {'id': r[0], 'date': r[1], 'category': r[2], 'amount': r[3], 'description': r[4]}
        for r in rows
    ]


@app.post('/expenses', response_model=ExpenseResponse, status_code=201, tags=['Расходы'])
def add_expense(expense: ExpenseCreate):
    """Добавить новый расход."""
    if expense.category not in CATEGORIES:
        raise HTTPException(status_code=400, detail=f'Неизвестная категория: {expense.category}')
    with get_connection() as conn:
        cursor = conn.execute(
            'INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)',
            (expense.date, expense.category, expense.amount, expense.description)
        )
        conn.commit()
        row = conn.execute(
            'SELECT id, date, category, amount, description FROM expenses WHERE id=?',
            (cursor.lastrowid,)
        ).fetchone()
    return {'id': row[0], 'date': row[1], 'category': row[2], 'amount': row[3], 'description': row[4]}


@app.delete('/expenses/{expense_id}', tags=['Расходы'])
def delete_expense(expense_id: int):
    """Удалить расход по ID."""
    with get_connection() as conn:
        row = conn.execute('SELECT id FROM expenses WHERE id=?', (expense_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f'Расход с id={expense_id} не найден')
        conn.execute('DELETE FROM expenses WHERE id=?', (expense_id,))
        conn.commit()
    return {'message': f'Расход {expense_id} удалён'}


@app.get('/stats', tags=['Статистика'])
def get_stats():
    """Статистика расходов по категориям."""
    with get_connection() as conn:
        rows = conn.execute(
            'SELECT category, SUM(amount), COUNT(*) FROM expenses GROUP BY category ORDER BY SUM(amount) DESC'
        ).fetchall()
        total = conn.execute('SELECT SUM(amount) FROM expenses').fetchone()[0] or 0
    result = []
    for row in rows:
        pct = (row[1] / total * 100) if total > 0 else 0
        result.append({
            'category': row[0],
            'total': round(row[1], 2),
            'count': row[2],
            'percent': round(pct, 1),
        })
    return {'total': round(total, 2), 'by_category': result}


@app.get('/stats/monthly', tags=['Статистика'])
def get_monthly_stats():
    """Статистика расходов по месяцам."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT substr(date, 7, 4) || '-' || substr(date, 4, 2) as month, "
            "SUM(amount), COUNT(*) FROM expenses GROUP BY month ORDER BY month"
        ).fetchall()
    return {
        'monthly': [
            {'month': r[0], 'total': round(r[1], 2), 'count': r[2]}
            for r in rows
        ]
    }


# ─────────────────────────────────────────────
# Запуск
# ─────────────────────────────────────────────

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
