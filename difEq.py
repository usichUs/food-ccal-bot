#python -m venv venv (если не работает, то похуй, можно без этого)
import numpy as np #pip install numpy
import matplotlib.pyplot as plt #pip install matplotlib
from scipy.integrate import odeint #pip install scipy

# Определяем функцию правых частей системы
def system(y, t):
    x, y = y
    dxdt = 3*x - 2*y #Менять тут (x с точкой)
    dydt = 4*y - 6*x #Менять тут (y с точкой)
    return [dxdt, dydt]

# Генерируем сетку для x и y
x = np.linspace(-2, 2, 20)
y = np.linspace(-2, 2, 20)

X, Y = np.meshgrid(x, y)

# Вычисляем значения производных на сетке
DX, DY = system([X, Y], 0)

# Рисуем фазовый портрет
plt.streamplot(X, Y, DX, DY, color='b', linewidth=1, arrowsize=1)
plt.plot(0, 0, 'ro')  # Отмечаем особую точку (0, 0)
plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Фазовый портрет')
plt.grid(True)
plt.show()