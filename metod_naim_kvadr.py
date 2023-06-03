import numpy as np

param = int(input())
sum_l = (param - 1) * 2

x = input()
x = x.split(' ')
x = [float(i) for i in x]

y = input()
y = y.split(' ')
y = [float(i) for i in y]

n = len(x)

s = []
for i in range(1, sum_l + 1):
    s.append(sum([j**i for j in x]))
s.reverse()
s.append(n)

p = []
for i in range(param):
    p.append(sum([a**i * b for (a, b) in zip(x, y)]))
p.reverse()

matr = []
for i in range(param):
    matr.append(s[i:i+param])

expr = np.array(matr)

abcde = np.linalg.solve(expr, p)

print(abcde)

