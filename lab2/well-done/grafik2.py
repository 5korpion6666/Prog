import plotly.graph_objects as go
import numpy as np

x1 = np.linspace(0, 1.5, 500)
x2 = np.linspace(1.51, 3, 500)

y1 = 2**x1 - 2 + x1**2
y2 = np.sqrt(x2) * np.exp(-x2**2)

x0 = 1.0
y0 = 2**x0 - 2 + x0**2
k = 2**x0 * np.log(2) + 2*x0
y_tangent = y0 + k * (x1 - x0)

fig = go.Figure()

fig.add_trace(go.Scatter(x=x1, y=y1, mode='lines', name='2^x - 2 + x²'))
fig.add_trace(go.Scatter(x=x2, y=y2, mode='lines', name='√x · e^(-x²)'))
fig.add_trace(go.Scatter(x=x1, y=y_tangent, mode='lines', name='Касательная', 
                        line=dict(color='red', dash='dash')))
fig.add_trace(go.Scatter(x=[x0], y=[y0], mode='markers', name='Точка касания',
                        marker=dict(color='red', size=8)))

fig.add_annotation(x=x0, y=y0, text=f'({x0}, {y0:.3f})',
                  showarrow=True, arrowhead=2, ax=100, ay=-50)

fig.update_layout(title='Вариант 5',
                 xaxis_title='x',
                 yaxis_title='f(x)',
                 showlegend=True,
                 xaxis=dict(showgrid=True, gridcolor='lightgray'),
                 yaxis=dict(showgrid=True, gridcolor='lightgray'))

fig.write_html('plot.html')
fig.show()