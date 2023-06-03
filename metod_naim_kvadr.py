import numpy as np


x = input()
x = x.split(' ')
x = [int(i) for i in x]

y = input()
y = y.split(' ')
y = [int(i) for i in y]

n = len(x)

s1 = sum([i for i in x])
s2 = sum([i**2 for i in x])
s3 = sum([i**3 for i in x])
s4 = sum([i**4 for i in x])
s5 = sum([i**5 for i in x])
s6 = sum([i**6 for i in x])
s7 = sum([i**7 for i in x])
s8 = sum([i**8 for i in x])

p1 = sum([j for (i, j) in zip(x, y)])
p2 = sum([i * j for (i, j) in zip(x, y)])
p3 = sum([i**2 * j for (i, j) in zip(x, y)])
p4 = sum([i**3 * j for (i, j) in zip(x, y)])
p5 = sum([i**4 * j for (i, j) in zip(x, y)])

expr = np.array([s8, s7, s6, s5, s4, s7, s6, s5, s4, s3, s6, s5, s4, s3, s2, s5, s4, s3, s2, s1, s4, s3, s2, s1, n])
expr = expr.reshape((5, 5))
fcol = np.array([p5, p4, p3, p2, p1])

abcde = np.linalg.solve(expr, fcol)

print(abcde)

