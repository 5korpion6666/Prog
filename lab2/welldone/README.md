# Лабораторная работа №2
## Построение графиков в Python — Well-done (Plotly)

## 1. Условие задачи

Создать интерактивный график по заданию с помощью Plotly, доступный всем по ссылке.

Функция варианта:

$$f(x) = \begin{cases} 2^x - 2 + x^2, & 0 \leq x \leq 1.5 \\ \sqrt{x} \cdot e^{-x^2}, & 1.5 < x \leq 3 \end{cases}$$

---

## 2. Описание проделанной работы

1. Построил интерактивный график через `plotly.graph_objects`
2. Добавил две части функции, касательную и точку касания как отдельные трассы (`go.Scatter`)
3. Добавил аннотацию к точке касания через `fig.add_annotation`
4. Сохранил график как `index.html` — полностью автономный интерактивный файл
5. Опубликовал на GitHub Pages

```python
import plotly.graph_objects as go

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x1, y=f(x1),
    mode='lines',
    name='f(x) = 2ˣ − 2 + x², [0; 1.5]',
    line=dict(color='#2196F3', width=2.5),
))

fig.write_html('lab2_plotly.html')
fig.show()
```

### Установка зависимостей

```bash
py -m pip install plotly
```

### Запуск

```bash
py lab2_welldone.py
```

---

## 3. Интерактивный график

🔗 **[Открыть график](https://5korpion6666.github.io/)**

Возможности интерактивного графика:
- Масштабирование колёсиком мыши
- Перемещение графика мышью
- Наведение на линию показывает координаты точки
- Скрытие/показ линий через легенду

<img width="1367" height="863" alt="лаб2_welldone" src="https://github.com/user-attachments/assets/cea49855-57a2-4c22-b553-005a5bb0271d" />


---

## 4. Используемые материалы

1. [Plotly — документация](https://plotly.com/python/)
2. [Plotly graph_objects](https://plotly.com/python/graph-objects/)
3. [GitHub Pages](https://pages.github.com/)
