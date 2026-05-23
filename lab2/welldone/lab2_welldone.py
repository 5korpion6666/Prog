# lab2_welldone.py — Plotly интерактивный график

import numpy as np
import plotly.graph_objects as go


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

fig = go.Figure()

# Первая часть функции
fig.add_trace(go.Scatter(
    x=x1, y=f(x1),
    mode='lines',
    name='f(x) = 2ˣ − 2 + x², [0; 1.5]',
    line=dict(color='#2196F3', width=2.5),
))

# Вторая часть функции
fig.add_trace(go.Scatter(
    x=x2, y=f(x2),
    mode='lines',
    name='f(x) = √x · e^(−x²), (1.5; 3]',
    line=dict(color='#4CAF50', width=2.5),
))

# Касательная
fig.add_trace(go.Scatter(
    x=x_tan, y=tangent(x_tan),
    mode='lines',
    name=f'Касательная в x₀ = {x0}',
    line=dict(color='#F44336', width=2, dash='dash'),
))

# Точка касания
fig.add_trace(go.Scatter(
    x=[x0], y=[y0],
    mode='markers',
    name='Точка касания',
    marker=dict(color='#F44336', size=10, symbol='circle'),
    showlegend=True,
))

# Аннотация
fig.add_annotation(
    x=x0, y=y0,
    text=f'<b>Точка касания</b><br>x₀ = {x0}<br>y₀ = {y0:.3f}<br>k = {slope:.3f}',
    showarrow=True,
    arrowhead=2,
    arrowcolor='black',
    ax=60, ay=-60,
    bgcolor='lightyellow',
    bordercolor='gray',
    borderwidth=1,
    font=dict(size=12),
)

fig.update_layout(
    title=dict(
        text='График функции f(x) и касательная',
        font=dict(size=18),
        x=0.5,
    ),
    xaxis=dict(title='x', showgrid=True, gridcolor='lightgray', zeroline=True),
    yaxis=dict(title='f(x)', showgrid=True, gridcolor='lightgray', zeroline=True),
    legend=dict(font=dict(size=12), bgcolor='rgba(255,255,255,0.8)', bordercolor='gray', borderwidth=1),
    plot_bgcolor='white',
    width=900,
    height=550,
)

# Сохранить как HTML (интерактивный)
fig.write_html('lab2_plotly.html')
print('Интерактивный график сохранён: lab2_plotly.html')

# Показать в браузере
fig.show()
