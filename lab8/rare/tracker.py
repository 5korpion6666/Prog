# tracker.py — Финансовый трекер расходов (Rare)

import sys
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit,
    QTableWidget, QTableWidgetItem, QTabWidget, QGroupBox,
    QHeaderView, QMessageBox, QStatusBar, QDoubleSpinBox,
    QSplitter, QFrame
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt6.QtGui import QPainter


CATEGORIES = ['Еда', 'Транспорт', 'Жильё', 'Развлечения', 'Здоровье', 'Одежда', 'Прочее']
COLORS = {
    'Еда': '#4CAF50',
    'Транспорт': '#2196F3',
    'Жильё': '#FF9800',
    'Развлечения': '#9C27B0',
    'Здоровье': '#F44336',
    'Одежда': '#00BCD4',
    'Прочее': '#607D8B',
}

# In-memory хранилище (Medium — заменим на SQLite)
expenses = []


def add_expense(date, category, amount, description):
    expenses.append({
        'id': len(expenses) + 1,
        'date': date,
        'category': category,
        'amount': amount,
        'description': description,
    })


def get_all_expenses():
    return list(reversed(expenses))


def delete_expense(expense_id):
    global expenses
    expenses = [e for e in expenses if e['id'] != expense_id]


def get_total():
    return sum(e['amount'] for e in expenses)


def get_by_category():
    result = {}
    for e in expenses:
        result[e['category']] = result.get(e['category'], 0) + e['amount']
    return result


# ─────────────────────────────────────────────
# Главное окно
# ─────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Финансовый трекер')
        self.setMinimumSize(900, 650)
        self._build_ui()

    def _build_ui(self):
        tabs = QTabWidget()
        tabs.addTab(self._tab_expenses(), 'Расходы')
        tabs.addTab(self._tab_charts(), 'Графики')
        self.setCentralWidget(tabs)
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self._update_status()

    # ── Вкладка 1: Расходы ──────────────────────

    def _tab_expenses(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Форма добавления
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

        # Фильтр
        filter_group = QGroupBox('Фильтр')
        filter_layout = QHBoxLayout(filter_group)

        filter_layout.addWidget(QLabel('Категория:'))
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(['Все'] + CATEGORIES)
        self.filter_combo.currentTextChanged.connect(self._apply_filter)
        filter_layout.addWidget(self.filter_combo)

        clear_btn = QPushButton('Сбросить фильтр')
        clear_btn.clicked.connect(lambda: self.filter_combo.setCurrentText('Все'))
        filter_layout.addWidget(clear_btn)
        filter_layout.addStretch()

        layout.addWidget(filter_group)

        # Таблица
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

        add_expense(date, category, amount, description)
        self.desc_edit.clear()
        self._refresh_table()
        self._update_status()
        self.status.showMessage(f'Добавлено: {category} — {amount:.2f} ₽')

    def _refresh_table(self):
        selected_category = self.filter_combo.currentText()
        data = get_all_expenses()
        if selected_category != 'Все':
            data = [e for e in data if e['category'] == selected_category]

        self.table.setRowCount(0)
        for e in data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(e['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(e['date']))
            item_cat = QTableWidgetItem(e['category'])
            item_cat.setForeground(QColor(COLORS.get(e['category'], '#000')))
            self.table.setItem(row, 2, item_cat)
            self.table.setItem(row, 3, QTableWidgetItem(f"{e['amount']:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(e['description']))

    def _apply_filter(self):
        self._refresh_table()

    def _delete_selected(self):
        rows = self.table.selectedItems()
        if not rows:
            return
        row = self.table.currentRow()
        expense_id = int(self.table.item(row, 0).text())
        delete_expense(expense_id)
        self._refresh_table()
        self._update_status()
        self.status.showMessage('Запись удалена.')

    def _update_status(self):
        total = get_total()
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
        data = get_by_category()
        if not data:
            self.status.showMessage('Нет данных для графиков.')
            return

        # Круговая диаграмма
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

        # Столбчатая диаграмма
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


# ─────────────────────────────────────────────
# Запуск
# ─────────────────────────────────────────────

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
