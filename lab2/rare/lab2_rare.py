# lab2_rare.py

import numpy as np
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────
# Функция и её производная
# f(x) = 2^x - 2 + x^2,     0 <= x <= 1.5
# f(x) = sqrt(x) * e^(-x^2), 1.5 < x <= 3
# ─────────────────────────────────────────────

def f(x):
    return np.where(
        x <= 1.5,
        2**x - 2 + x**2,
        np.sqrt(x) * np.exp(-x**2)
    )


def df(x):
    """Производная для первой части: f'(x) = 2^x * ln(2) + 2x"""
    return 2**x * np.log(2) + 2 * x


# Точка касания (выбираем x0 = 1.0 — середина первого участка)
x0 = 1.0
y0 = f(x0)
slope = df(x0)

# Касательная: y = f(x0) + f'(x0) * (x - x0)
def tangent(x):
    return y0 + slope * (x - x0)


# ─────────────────────────────────────────────
# Построение графика
# ─────────────────────────────────────────────

x1 = np.linspace(0, 1.5, 400)
x2 = np.linspace(1.5, 3, 400)
x_all = np.linspace(0, 3, 800)
x_tan = np.linspace(0.4, 1.6, 200)

fig, ax = plt.subplots(figsize=(10, 6))

# График функции
ax.plot(x1, f(x1), 'b-', linewidth=2, label=r'$f(x) = 2^x - 2 + x^2$, $0 \leq x \leq 1.5$')
ax.plot(x2, f(x2), 'g-', linewidth=2, label=r'$f(x) = \sqrt{x} \cdot e^{-x^2}$, $1.5 < x \leq 3$')

# Касательная
ax.plot(x_tan, tangent(x_tan), 'r--', linewidth=1.5, label=f'Касательная в $x_0 = {x0}$')

# Точка касания
ax.plot(x0, y0, 'ro', markersize=8, zorder=5)

# Аннотация
ax.annotate(
    f'Точка касания\n$x_0 = {x0}$, $y_0 = {y0:.3f}$\n$k = {slope:.3f}$',
    xy=(x0, y0),
    xytext=(x0 + 0.4, y0 - 0.3),
    fontsize=10,
    arrowprops=dict(arrowstyle='->', color='black'),
    bbox=dict(boxstyle='round,pad=0.3', fc='lightyellow', ec='gray'),
)

# Оформление
ax.set_title('График функции $f(x)$ и касательная', fontsize=14)
ax.set_xlabel('$x$', fontsize=12)
ax.set_ylabel('$f(x)$', fontsize=12)
ax.legend(fontsize=10)
ax.grid(True, linestyle='--', alpha=0.6)
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)

plt.tight_layout()
plt.savefig('lab2_plot.png', dpi=150)
plt.show()
print('График сохранён: lab2_plot.png')
