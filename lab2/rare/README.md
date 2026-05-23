# Лабораторная работа №2
## Построение графиков в Python

## 1. Условие задачи

Выбрать одну из неразрывных функций своего варианта, построить график и касательную к ней. Добавить заголовок, подписи осей, легенду, сетку и аннотацию к точке касания.

Функция варианта:

$$f(x) = \begin{cases} 2^x - 2 + x^2, & 0 \leq x \leq 1.5 \\ \sqrt{x} \cdot e^{-x^2}, & 1.5 < x \leq 3 \end{cases}$$

---

## 2. Описание проделанной работы

Выбрана первая часть функции $f(x) = 2^x - 2 + x^2$ на отрезке $[0, 1.5]$ — она непрерывна и дифференцируема.

Производная первой части:

$$f'(x) = 2^x \cdot \ln 2 + 2x$$

Точка касания: $x_0 = 1.0$

Уравнение касательной:

$$y = f(x_0) + f'(x_0) \cdot (x - x_0)$$

```python
import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return np.where(
        x <= 1.5,
        2**x - 2 + x**2,
        np.sqrt(x) * np.exp(-x**2)
    )

def df(x):
    return 2**x * np.log(2) + 2 * x

x0 = 1.0
y0 = f(x0)
slope = df(x0)

def tangent(x):
    return y0 + slope * (x - x0)
```

### Установка зависимостей

```bash
py -m venv env
env\Scripts\activate
py -m pip install -r requirements.txt
```

### Запуск

```bash
py lab2_rare.py
```

---

## 3. График

<img width="993" height="594" alt="лаб2_rare" src="https://github.com/user-attachments/assets/2646117a-7e04-463a-8eca-fd23d7a3825d" />

---

## 4. Используемые материалы

1. [Devpractice Team. Библиотека Matplotlib](https://evil-teacher.orbiter.website/books/prog_pm/matplotlib.pdf)
2. [Matplotlib — документация](https://matplotlib.org/)
3. [NumPy — документация](https://numpy.org/doc/)
