import numpy as np

num_of_params = int(input())
num_of_sums = (num_of_params - 1) * 2

x = input()
x = x.split(' ')
x = [float(i) for i in x]

y = input()
y = y.split(' ')
y = [float(i) for i in y]

n = len(x)

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

print(output)

