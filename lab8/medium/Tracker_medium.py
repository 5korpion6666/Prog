# tracker.py — Финансовый трекер расходов (Medium — SQLite)

import sys
import sqlite3
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit,
    QTableWidget, QTableWidgetItem, QTabWidget, QGroupBox,
    QHeaderView, QMessageBox, QStatusBar, QDoubleSpinBox,
    QSplitter
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QColor, QPainter
from PyQt6.QtCharts import (
    QChart, QChartView, QPieSeries,
    QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
)

CATEGORIES = ['Еда', 'Транспорт', 'Жильё', 'Развлечения', 'Здоровье', 'Одежда', 'Прочее']
COLORS = {
    'Еда': '#4CAF50', 'Транспорт': '#2196F3', 'Жильё': '#FF9800',
    'Развлечения': '#9C27B0', 'Здоровье': '#F44336',
    'Одежда': '#00BCD4', 'Прочее': '#607D8B',
}
DB_PATH = 'tracker.db'


# ─────────────────────────────────────────────
# Слой работы с БД
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


def db_add_expense(date, category, amount, description):
    with get_connection() as conn:
        conn.execute(
            'INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)',
            (date, category, amount, description)
        )
        conn.commit()


def db_get_all(category_filter=None):
    with get_connection() as conn:
        if category_filter and category_filter != 'Все':
            rows = conn.execute(
                'SELECT id, date, category, amount, description FROM expenses WHERE category=? ORDER BY id DESC',
                (category_filter,)
            ).fetchall()
        else:
            rows = conn.execute(
                'SELECT id, date, category, amount, description FROM expenses ORDER BY id DESC'
            ).fetchall()
    return rows


def db_delete(expense_id):
    with get_connection() as conn:
        conn.execute('DELETE FROM expenses WHERE id=?', (expense_id,))
        conn.commit()


def db_get_total():
    with get_connection() as conn:
        result = conn.execute('SELECT SUM(amount) FROM expenses').fetchone()[0]
    return result or 0.0


def db_get_by_category():
    with get_connection() as conn:
        rows = conn.execute(
            'SELECT category, SUM(amount) FROM expenses GROUP BY category'
        ).fetchall()
    return {row[0]: row[1] for row in rows}


def db_get_monthly():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT substr(date, 7, 4) || '-' || substr(date, 4, 2) as month, SUM(amount) "
            "FROM expenses GROUP BY month ORDER BY month"
        ).fetchall()
    return rows


# ─────────────────────────────────────────────
# Главное окно
# ─────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Финансовый трекер')
        self.setMinimumSize(900, 650)
        init_db()
        self._build_ui()
        self._refresh_table()
        self._update_status()

    def _build_ui(self):
        tabs = QTabWidget()
        tabs.addTab(self._tab_expenses(), 'Расходы')
        tabs.addTab(self._tab_charts(), 'Графики')
        tabs.addTab(self._tab_stats(), 'Статистика')
        self.setCentralWidget(tabs)
        self.status = QStatusBar()
        self.setStatusBar(self.status)

    # ── Вкладка 1: Расходы ──────────────────────

    def _tab_expenses(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        group = QGroupBox('Добавить расход')
        form = QHBoxLayout(group)

        form.addWidget(QLabel('Дата:'))
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat('dd.MM.yyyy')
        form.addWidget(self.date_edit)

        form.addWidget(QLabel('Категория:'))
        self.category_combo = QComboBox()
        self.category_combo.addItems(CATEGORIES)
        form.addWidget(self.category_combo)

        form.addWidget(QLabel('Сумма (₽):'))
        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setRange(0.01, 1_000_000)
        self.amount_spin.setDecimals(2)
        self.amount_spin.setValue(100)
        form.addWidget(self.amount_spin)

        form.addWidget(QLabel('Описание:'))
        self.desc_edit = QLineEdit()
        self.desc_edit.setPlaceholderText('Необязательно')
        form.addWidget(self.desc_edit)

        add_btn = QPushButton('Добавить')
        add_btn.clicked.connect(self._add_expense)
        form.addWidget(add_btn)

        layout.addWidget(group)

        filter_group = QGroupBox('Фильтр')
        filter_layout = QHBoxLayout(filter_group)
        filter_layout.addWidget(QLabel('Категория:'))
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(['Все'] + CATEGORIES)
        self.filter_combo.currentTextChanged.connect(self._refresh_table)
        filter_layout.addWidget(self.filter_combo)
        clear_btn = QPushButton('Сбросить')
        clear_btn.clicked.connect(lambda: self.filter_combo.setCurrentText('Все'))
        filter_layout.addWidget(clear_btn)
        filter_layout.addStretch()
        layout.addWidget(filter_group)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(['ID', 'Дата', 'Категория', 'Сумма (₽)', 'Описание'])
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(0, 40)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 120)
        self.table.setColumnWidth(3, 100)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.table)

        del_btn = QPushButton('Удалить выбранное')
        del_btn.clicked.connect(self._delete_selected)
        layout.addWidget(del_btn)

        return widget

    def _add_expense(self):
        date = self.date_edit.date().toString('dd.MM.yyyy')
        category = self.category_combo.currentText()
        amount = self.amount_spin.value()
        description = self.desc_edit.text().strip()
        db_add_expense(date, category, amount, description)
        self.desc_edit.clear()
        self._refresh_table()
        self._update_status()
        self.status.showMessage(f'Добавлено: {category} — {amount:.2f} ₽')

    def _refresh_table(self):
        selected_category = self.filter_combo.currentText()
        rows = db_get_all(selected_category)
        self.table.setRowCount(0)
        for e in rows:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(e[0])))
            self.table.setItem(row, 1, QTableWidgetItem(e[1]))
            item_cat = QTableWidgetItem(e[2])
            item_cat.setForeground(QColor(COLORS.get(e[2], '#000')))
            self.table.setItem(row, 2, item_cat)
            self.table.setItem(row, 3, QTableWidgetItem(f'{e[3]:.2f}'))
            self.table.setItem(row, 4, QTableWidgetItem(e[4]))

    def _delete_selected(self):
        row = self.table.currentRow()
        if row < 0:
            return
        expense_id = int(self.table.item(row, 0).text())
        db_delete(expense_id)
        self._refresh_table()
        self._update_status()
        self.status.showMessage('Запись удалена.')

    def _update_status(self):
        total = db_get_total()
        self.setWindowTitle(f'Финансовый трекер — Итого: {total:.2f} ₽')

    # ── Вкладка 2: Графики ──────────────────────

    def _tab_charts(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        refresh_btn = QPushButton('Обновить графики')
        refresh_btn.clicked.connect(self._refresh_charts)
        layout.addWidget(refresh_btn)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.pie_view = QChartView()
        self.pie_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        splitter.addWidget(self.pie_view)
        self.bar_view = QChartView()
        self.bar_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        splitter.addWidget(self.bar_view)
        layout.addWidget(splitter)
        return widget

    def _refresh_charts(self):
        data = db_get_by_category()
        if not data:
            self.status.showMessage('Нет данных для графиков.')
            return

        pie = QPieSeries()
        for cat, total in data.items():
            slc = pie.append(f'{cat}\n{total:.0f} ₽', total)
            slc.setColor(QColor(COLORS.get(cat, '#607D8B')))
            slc.setLabelVisible(True)
        pie_chart = QChart()
        pie_chart.addSeries(pie)
        pie_chart.setTitle('Расходы по категориям')
        pie_chart.legend().setVisible(False)
        self.pie_view.setChart(pie_chart)

        bar_set = QBarSet('Сумма (₽)')
        categories = list(data.keys())
        for cat in categories:
            bar_set.append(data[cat])
        bar_set.setColor(QColor('#2196F3'))
        bar_series = QBarSeries()
        bar_series.append(bar_set)
        bar_chart = QChart()
        bar_chart.addSeries(bar_series)
        bar_chart.setTitle('Сравнение по категориям')
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        bar_chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        bar_series.attachAxis(axis_x)
        axis_y = QValueAxis()
        bar_chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        bar_series.attachAxis(axis_y)
        bar_chart.legend().setVisible(False)
        self.bar_view.setChart(bar_chart)
        self.status.showMessage('Графики обновлены.')

    # ── Вкладка 3: Статистика ───────────────────

    def _tab_stats(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        refresh_btn = QPushButton('Обновить статистику')
        refresh_btn.clicked.connect(self._refresh_stats)
        layout.addWidget(refresh_btn)

        self.stats_table = QTableWidget(0, 3)
        self.stats_table.setHorizontalHeaderLabels(['Категория', 'Сумма (₽)', 'Доля (%)'])
        self.stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.stats_table)

        self.monthly_view = QChartView()
        self.monthly_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.monthly_view.setMinimumHeight(200)
        layout.addWidget(self.monthly_view)

        return widget

    def _refresh_stats(self):
        data = db_get_by_category()
        total = db_get_total()

        self.stats_table.setRowCount(0)
        for cat, amount in sorted(data.items(), key=lambda x: x[1], reverse=True):
            row = self.stats_table.rowCount()
            self.stats_table.insertRow(row)
            item_cat = QTableWidgetItem(cat)
            item_cat.setForeground(QColor(COLORS.get(cat, '#000')))
            self.stats_table.setItem(row, 0, item_cat)
            self.stats_table.setItem(row, 1, QTableWidgetItem(f'{amount:.2f}'))
            pct = (amount / total * 100) if total > 0 else 0
            self.stats_table.setItem(row, 2, QTableWidgetItem(f'{pct:.1f}%'))

        monthly = db_get_monthly()
        if monthly:
            bar_set = QBarSet('Расходы (₽)')
            months = []
            for month, amount in monthly:
                bar_set.append(amount)
                months.append(month)
            bar_set.setColor(QColor('#FF9800'))
            series = QBarSeries()
            series.append(bar_set)
            chart = QChart()
            chart.addSeries(series)
            chart.setTitle('Расходы по месяцам')
            axis_x = QBarCategoryAxis()
            axis_x.append(months)
            chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
            series.attachAxis(axis_x)
            axis_y = QValueAxis()
            chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
            series.attachAxis(axis_y)
            chart.legend().setVisible(False)
            self.monthly_view.setChart(chart)

        self.status.showMessage('Статистика обновлена.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
