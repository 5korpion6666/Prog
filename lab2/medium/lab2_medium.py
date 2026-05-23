# lab2_medium.py — Seaborn версия

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def f(x):
    return np.where(
        x <= 1.5,
        2**x - 2 + x**2,
        np.sqrt(x) * np.exp(-x**2)
    )


def df(x):
    return 2**x * np.log(2) + 2 * x


x0 = 1.0
y0 = float(f(x0))
slope = float(df(x0))


def tangent(x):
    return y0 + slope * (x - x0)


x1 = np.linspace(0, 1.5, 400)
x2 = np.linspace(1.5, 3, 400)
x_tan = np.linspace(0.4, 1.6, 200)

LABEL1 = 'f(x) = 2^x - 2 + x^2, [0; 1.5]'
LABEL2 = 'f(x) = sqrt(x)*e^(-x^2), (1.5; 3]'
LABEL3 = f'Касательная в x0 = {x0}'

df_part1 = pd.DataFrame({'x': x1,    'y': f(x1),       'label': LABEL1})
df_part2 = pd.DataFrame({'x': x2,    'y': f(x2),       'label': LABEL2})
df_tan   = pd.DataFrame({'x': x_tan, 'y': tangent(x_tan), 'label': LABEL3})
df_all   = pd.concat([df_part1, df_part2, df_tan], ignore_index=True)

sns.set_theme(style='whitegrid', palette='deep')

fig, ax = plt.subplots(figsize=(10, 6))

palette = {LABEL1: '#2196F3', LABEL2: '#4CAF50', LABEL3: '#F44336'}

sns.lineplot(
    data=df_all, x='x', y='y', hue='label',
    palette=palette, linewidth=2, ax=ax
)

# Делаем касательную пунктирной после построения
for line in ax.get_lines():
    if line.get_label() == LABEL3:
        line.set_linestyle('--')

ax.plot(x0, y0, 'o', color='#F44336', markersize=9, zorder=5)

ax.annotate(
    f'Точка касания\nx0 = {x0}, y0 = {y0:.3f}\nk = {slope:.3f}',
    xy=(x0, y0),
    xytext=(x0 + 0.4, y0 - 0.3),
    fontsize=10,
    arrowprops=dict(arrowstyle='->', color='black'),
    bbox=dict(boxstyle='round,pad=0.3', fc='lightyellow', ec='gray'),
)

ax.set_title('График функции f(x) и касательная (Seaborn)', fontsize=14)
ax.set_xlabel('x', fontsize=12)
ax.set_ylabel('f(x)', fontsize=12)
ax.legend(title='', fontsize=10)
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)

plt.tight_layout()
plt.savefig('lab2_seaborn.png', dpi=150)
plt.show()
print('График сохранён: lab2_seaborn.png')
