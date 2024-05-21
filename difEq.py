import decimal
import numpy as np
import random
import matplotlib.pyplot as plt

# Размер матрицы
n = 3

num_matrices = 1000

abs_diffs = []
num_inside = 0

# Инициализация матрицы
for _ in range(num_matrices):
    A = np.random.rand(n, n)
    decimal.getcontext().prec = 20
    # Вычисление определителя с помощью метода Монте-Карло

    m = 1000  # Количество случайных векторов

    det_sum = decimal.Decimal(0)
    
    
    for _ in range(m):
        # Генерация случайных векторов в пределах единичного куба
        x = np.random.rand(n, 1)
        y = np.random.rand(n, 1)
        z = np.random.rand(n, 1)
        
        # Проверка, выходят ли векторы за пределы единичного куба
        if np.all(x <= 1) and np.all(x >= 0) and np.all(y <= 1) and np.all(y >= 0) and np.all(z <= 1) and np.all(z >= 0):
            num_inside += 1
            
            # Вычисление определителя матрицы [x, y, z] с высокой точностью
            det = decimal.Decimal(np.linalg.det(np.hstack((x, y, z))))
            
            # Суммирование определителей
            det_sum += det
        
    # Приближение определителя
    det_approx = det_sum / decimal.Decimal(num_inside)
    
    # Вычисление истинного определителя
    det_true = decimal.Decimal(np.linalg.det(A))

    abs_diff = abs(det_true - det_approx)

    abs_diffs.append(abs_diff)

mean_error = np.mean(abs_diffs)


# Отображение результатов
print("Приближенный определитель:", det_approx)
print("Истинный определитель:", det_true)
print("srednyaya pogreshnost:", mean_error)

# Визуализация параллелепипеда
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Столбцы матрицы A представляют стороны параллелепипеда
ax.quiver(
    np.zeros(n), np.zeros(n), np.zeros(n),
    A[:, 0], A[:, 1], A[:, 2],
    color='red', alpha=0.5
)

# Отображение точек на поверхности параллелепипеда
for i in range(100):
    # Генерация случайных векторов в пределах единичного куба
    x = np.random.rand(n, 1)
    y = np.random.rand(n, 1)
    z = np.random.rand(n, 1)

    # Отображение точек
    ax.scatter(x[0], x[1], x[2], color='blue', alpha=0.1)
    ax.scatter(y[0], y[1], y[2], color='green', alpha=0.1)
    ax.scatter(z[0], z[1], z[2], color='purple', alpha=0.1)

plt.show()