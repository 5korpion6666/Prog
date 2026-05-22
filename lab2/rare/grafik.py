import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

x1 = np.linspace(0, 1.5, 500)
x2 = np.linspace(1.51, 3, 500)

y1 = 2**x1 - 2 + x1**2
y2 = np.sqrt(x2) * np.exp(-x2**2)

x0 = 1.0
y0 = 2**x0 - 2 + x0**2
k = 2**x0 * np.log(2) + 2*x0
y_tangent = y0 + k * (x1 - x0)

plt.title('Вариант 5')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid()
plt.plot(x1, y1, label='2^x - 2 + x²')
plt.plot(x2, y2, label='√x · e^(-x²)')
plt.plot(x1, y_tangent, 'r--', label='Касательная')
plt.plot(x0, y0, 'ro')
plt.annotate(f'({x0}, {y0:.3f})', xy=(x0, y0), xytext=(x0+0.5, y0+1),
          arrowprops=dict(arrowstyle='->'))
plt.legend()
plt.savefig('plot.png', dpi=300)