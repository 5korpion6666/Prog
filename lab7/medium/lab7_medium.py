# lab7_medium.py

import sys
import threading
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox, QDoubleSpinBox,
    QTableWidget, QTableWidgetItem, QTabWidget, QGroupBox, QCheckBox,
    QTextEdit, QStatusBar, QHeaderView
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from lab7.generators import (
    exchange_rates_generator,
    exchange_rates_generator_threaded,
    rate_pairs_generator,
)
from lab7.recursion import split_iter, split_recursive, calc_rate_iterative, calc_rate_recursive


# ─────────────────────────────────────────────
# Воркер для запросов в отдельном потоке
# ─────────────────────────────────────────────

class FetchWorker(QThread):
    result_ready = pyqtSignal(list)
    error_occurred = pyqtSignal(str)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            results = list(self.func(*self.args, **self.kwargs))
            self.result_ready.emit(results)
        except Exception as e:
            self.error_occurred.emit(str(e))


# ─────────────────────────────────────────────
# Главное окно
# ─────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Курсы валют')
        self.setMinimumSize(800, 600)
        self._build_ui()

    def _build_ui(self):
        tabs = QTabWidget()
        tabs.addTab(self._tab_rates(), 'Курсы валют')
        tabs.addTab(self._tab_pair(), 'Пара валют')
        tabs.addTab(self._tab_split(), 'Split')
        tabs.addTab(self._tab_calc(), 'Расчёт курса')
        self.setCentralWidget(tabs)
        self.status = QStatusBar()
        self.setStatusBar(self.status)

    # ── Вкладка 1: Курсы валют ──────────────────

    def _tab_rates(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Настройки
        group = QGroupBox('Параметры')
        form = QHBoxLayout(group)

        form.addWidget(QLabel('Валюты:'))
        self.rates_input = QLineEdit('USD,EUR,GBP')
        form.addWidget(self.rates_input)

        form.addWidget(QLabel('Цель:'))
        self.rates_target = QComboBox()
        self.rates_target.addItems(['RUB', 'USD', 'EUR', 'GBP', 'JPY', 'CNY'])
        form.addWidget(self.rates_target)

        self.rates_threaded = QCheckBox('Многопоточный')
        form.addWidget(self.rates_threaded)

        form.addWidget(QLabel('Потоков:'))
        self.rates_workers = QSpinBox()
        self.rates_workers.setRange(1, 20)
        self.rates_workers.setValue(5)
        form.addWidget(self.rates_workers)

        layout.addWidget(group)

        self.rates_btn = QPushButton('Получить курсы')
        self.rates_btn.clicked.connect(self._fetch_rates)
        layout.addWidget(self.rates_btn)

        self.rates_table = QTableWidget(0, 2)
        self.rates_table.setHorizontalHeaderLabels(['Базовая валюта', 'Курс'])
        self.rates_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.rates_table)

        return widget

    def _fetch_rates(self):
        currencies = [c.strip().upper() for c in self.rates_input.text().split(',')]
        target = self.rates_target.currentText()
        threaded = self.rates_threaded.isChecked()
        workers = self.rates_workers.value()

        self.rates_btn.setEnabled(False)
        self.rates_table.setRowCount(0)
        self.status.showMessage('Загрузка...')

        gen_func = exchange_rates_generator_threaded if threaded else exchange_rates_generator
        args = (currencies, workers) if threaded else (currencies,)

        self._rates_worker = FetchWorker(gen_func, *args)
        self._rates_worker.result_ready.connect(lambda r: self._show_rates(r, target))
        self._rates_worker.error_occurred.connect(self._on_error)
        self._rates_worker.finished.connect(lambda: self.rates_btn.setEnabled(True))
        self._rates_worker.start()

    def _show_rates(self, results, target):
        self.rates_table.setHorizontalHeaderLabels(['Базовая валюта', f'1 BASE = ? {target}'])
        for result in results:
            row = self.rates_table.rowCount()
            self.rates_table.insertRow(row)
            if 'error' in result:
                self.rates_table.setItem(row, 0, QTableWidgetItem(result['base']))
                self.rates_table.setItem(row, 1, QTableWidgetItem(f'Ошибка: {result["error"]}'))
            else:
                rate = result['rates'].get(target, 'N/A')
                self.rates_table.setItem(row, 0, QTableWidgetItem(result['base']))
                self.rates_table.setItem(row, 1, QTableWidgetItem(str(rate)))
        self.status.showMessage(f'Готово. Получено {len(results)} результатов.')

    # ── Вкладка 2: Пара валют ───────────────────

    def _tab_pair(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        group = QGroupBox('Параметры')
        form = QHBoxLayout(group)

        form.addWidget(QLabel('Из:'))
        self.pair_from = QComboBox()
        self.pair_from.addItems(['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'CHF', 'CAD', 'AUD', 'RUB'])
        form.addWidget(self.pair_from)

        form.addWidget(QLabel('В:'))
        self.pair_to = QComboBox()
        self.pair_to.addItems(['RUB', 'USD', 'EUR', 'GBP', 'JPY', 'CNY', 'CHF', 'CAD', 'AUD'])
        form.addWidget(self.pair_to)

        layout.addWidget(group)

        btn = QPushButton('Получить курс')
        btn.clicked.connect(self._fetch_pair)
        layout.addWidget(btn)

        self.pair_result = QLabel('')
        self.pair_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(20)
        self.pair_result.setFont(font)
        layout.addWidget(self.pair_result)
        layout.addStretch()

        return widget

    def _fetch_pair(self):
        from_c = self.pair_from.currentText()
        to_c = self.pair_to.currentText()
        self.pair_result.setText('Загрузка...')
        self.status.showMessage('Загрузка...')

        self._pair_worker = FetchWorker(rate_pairs_generator, [(from_c, to_c)])
        self._pair_worker.result_ready.connect(self._show_pair)
        self._pair_worker.error_occurred.connect(self._on_error)
        self._pair_worker.start()

    def _show_pair(self, results):
        if results and 'error' not in results[0]:
            r = results[0]
            self.pair_result.setText(f'1 {r["from"]} = {r["rate"]} {r["to"]}')
            self.status.showMessage('Готово.')
        else:
            self.pair_result.setText('Ошибка')

    # ── Вкладка 3: Split ────────────────────────

    def _tab_split(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        group = QGroupBox('Параметры')
        form = QHBoxLayout(group)

        form.addWidget(QLabel('Валюты:'))
        self.split_input = QLineEdit('USD,EUR,GBP,JPY,CNY,RUB')
        form.addWidget(self.split_input)

        form.addWidget(QLabel('Частей:'))
        self.split_parts = QSpinBox()
        self.split_parts.setRange(1, 10)
        self.split_parts.setValue(3)
        form.addWidget(self.split_parts)

        self.split_recursive = QCheckBox('Рекурсивный')
        form.addWidget(self.split_recursive)

        layout.addWidget(group)

        btn = QPushButton('Разбить')
        btn.clicked.connect(self._do_split)
        layout.addWidget(btn)

        self.split_table = QTableWidget(0, 0)
        self.split_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.split_table)

        return widget

    def _do_split(self):
        currencies = [c.strip().upper() for c in self.split_input.text().split(',')]
        parts = self.split_parts.value()
        fn = split_recursive if self.split_recursive.isChecked() else split_iter
        result = fn(currencies, parts)

        self.split_table.setRowCount(1)
        self.split_table.setColumnCount(parts)
        self.split_table.setHorizontalHeaderLabels([f'Часть {i+1}' for i in range(parts)])
        for i, chunk in enumerate(result):
            self.split_table.setItem(0, i, QTableWidgetItem(', '.join(chunk)))
        self.status.showMessage('Готово.')

    # ── Вкладка 4: Расчёт курса ─────────────────

    def _tab_calc(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        group = QGroupBox('Параметры')
        form = QHBoxLayout(group)

        form.addWidget(QLabel('Шагов:'))
        self.calc_steps = QSpinBox()
        self.calc_steps.setRange(1, 100)
        self.calc_steps.setValue(10)
        form.addWidget(self.calc_steps)

        form.addWidget(QLabel('Начальный курс:'))
        self.calc_initial = QDoubleSpinBox()
        self.calc_initial.setRange(0.01, 10000)
        self.calc_initial.setValue(90.5)
        self.calc_initial.setDecimals(4)
        form.addWidget(self.calc_initial)

        self.calc_recursive = QCheckBox('Рекурсивный')
        form.addWidget(self.calc_recursive)

        layout.addWidget(group)

        btn = QPushButton('Вычислить')
        btn.clicked.connect(self._do_calc)
        layout.addWidget(btn)

        self.calc_result = QLabel('')
        self.calc_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(16)
        self.calc_result.setFont(font)
        layout.addWidget(self.calc_result)
        layout.addStretch()

        return widget

    def _do_calc(self):
        steps = self.calc_steps.value()
        initial = self.calc_initial.value()
        fn = calc_rate_recursive if self.calc_recursive.isChecked() else calc_rate_iterative
        mode = 'рекурсивная' if self.calc_recursive.isChecked() else 'итеративная'
        result = fn(steps, initial)
        self.calc_result.setText(f'Результат ({mode}): {result:.6f}')
        self.status.showMessage('Готово.')

    def _on_error(self, msg):
        self.status.showMessage(f'Ошибка: {msg}')


# ─────────────────────────────────────────────
# Запуск
# ─────────────────────────────────────────────

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
