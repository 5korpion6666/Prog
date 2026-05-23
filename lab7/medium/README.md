# Лабораторная работа №7
## Пакеты и модули

## 1. Условия задачи

### Задание (Medium)
Реализовать GUI приложение на одном из актуальных фреймворков.

---

## 2. Описание проделанной работы

Реализовал GUI приложение на PyQt6 с 4 вкладками на основе логики из пакета `lab7`:

1. **Курсы валют** — ввод списка валют, выбор целевой валюты, переключение однопоточного/многопоточного режима, результаты в таблице
2. **Пара валют** — выбор двух валют из списка, отображение курса крупным шрифтом
3. **Split** — разбивка списка валют на N частей (итеративно или рекурсивно)
4. **Расчёт курса** — рекуррентный расчёт изменения курса по формуле из лаб 4

Запросы к API выполняются в отдельном потоке через `QThread` — интерфейс не зависает во время загрузки.

```python
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
```

### Запуск

```bash
py -m pip install PyQt6
py lab7_medium.py
```

---

## 3. Скриншоты результатов

### Вкладка «Курсы валют»
<img width="802" height="629" alt="лаб7_курс" src="https://github.com/user-attachments/assets/658b061c-f224-4a45-808b-699498dc1ed1" />

### Вкладка «Пара валют»
<img width="796" height="622" alt="лаб7_пара" src="https://github.com/user-attachments/assets/fdaeb960-5531-4840-a5ac-ecd02e78db48" />

### Вкладка «Split»
<img width="801" height="626" alt="лаб7_сплит" src="https://github.com/user-attachments/assets/eb86da9b-62e3-4339-b893-f4553400ab61" />

### Вкладка «Расчёт курса»
<img width="797" height="627" alt="лаб7_расчёт_курса" src="https://github.com/user-attachments/assets/4b8da09f-97df-44e7-ba4b-a88b011e5919" />

---

## 4. Используемые материалы

1. [PyQt6 — документация](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
2. [QThread — документация](https://doc.qt.io/qt-6/qthread.html)
3. [Пакеты и модули Python — документация](https://docs.python.org/3/tutorial/modules.html)
