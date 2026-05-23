# Лабораторная работа №2
## Построение графиков в Python — Medium (Seaborn)

## 1. Условие задачи

Построить все графики с использованием Seaborn вместо Matplotlib.

Функция варианта:

$$f(x) = \begin{cases} 2^x - 2 + x^2, & 0 \leq x \leq 1.5 \\ \sqrt{x} \cdot e^{-x^2}, & 1.5 < x \leq 3 \end{cases}$$

---

## 2. Описание проделанной работы

1. Данные для графика подготовлены в виде `pandas.DataFrame` с колонкой `label` — это позволяет `seaborn.lineplot` автоматически строить легенду
2. Применена тема `sns.set_theme(style='whitegrid')` — заменяет стандартную сетку Matplotlib на более аккуратную seaborn-сетку
3. Касательная отрисована пунктиром через `line.set_linestyle('--')` после построения
4. Аннотация точки касания добавлена через `ax.annotate`

```python
import seaborn as sns
import pandas as pd

sns.set_theme(style='whitegrid', palette='deep')

df_all = pd.concat([df_part1, df_part2, df_tan], ignore_index=True)

sns.lineplot(
    data=df_all, x='x', y='y', hue='label',
    palette=palette, linewidth=2, ax=ax
)
```

### Установка зависимостей

```bash
py -m pip install matplotlib numpy seaborn pandas
```

### Запуск

```bash
py lab2_medium.py
```

---

## 3. График

<img width="994" height="591" alt="лаб2_medium" src="https://github.com/user-attachments/assets/ea917572-9e61-44d8-b789-6d03a9163327" />

---

## 4. Используемые материалы

1. [Seaborn — документация](https://seaborn.pydata.org/)
2. [Seaborn lineplot](https://seaborn.pydata.org/generated/seaborn.lineplot.html)
3. [Pandas DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
