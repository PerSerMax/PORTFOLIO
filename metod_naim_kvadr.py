import matplotlib.pyplot as plt
import numpy as np


def meth_naim_kv(x, y, num_of_params):
    num_of_sums = (num_of_params - 1) * 2
    s = []
    for i in range(1, num_of_sums + 1):
        s.append(sum([j**i for j in x]))
    s.reverse()
    s.append(n)

    p = []
    for i in range(num_of_params):
        p.append(sum([a**i * b for (a, b) in zip(x, y)]))
    p.reverse()

    matrix = []
    for i in range(num_of_params):
        matrix.append(s[i:i + num_of_params])

    expr = np.array(matrix)

    output = np.linalg.solve(expr, p)

    for i in range(num_of_params):
        if abs(output[i] - int(output[i])) < 10**(-14):
            output[i] = int(output[i])

    return output


n_p = 4  #Количество параметров

x = input('')
x = x.split(' ')
x = [float(i) for i in x]

y = input()
y = y.split(' ')
y = [float(i) for i in y]

n = len(x)

params = list(meth_naim_kv(x,  y, n_p))
params.reverse()

plt.scatter(x, y)
D = np.arange(min(x) - (max(x) - min(x)), max(x) + (max(x) - min(x)), 0.1)
expr = 0

for i in range(n_p - 1, -1, -1):
    expr += params[i] * D**i

plt.plot(D, expr)
plt.show()