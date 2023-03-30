import re


class Sym:
    def __init__(self, s):
        for i in s:




def symbMul(a, b):
    res = [int]
    res[0] = a[0] * b[0]
    res.append(*a[1:])
    res.append(*b[1:])
    return res


def rasbNaSkob(a):
    res = []
    a = a.replace(' ', '')
    i = 0
    while i < len(a):
        if a[i] == '(':
            for j in range(i, len(a)):
                if a[j] == ')':
                    res.append(a[i + 1:j])
                    i = j + 1
                    break
        else:
            i += 1
    return res


def rasbNaSlag(a):
    return a.split('+')


a = '   (3a+5b+c)   (a + b+2c)(a+b+c)    '
a = rasbNaSkob(a)
print(a)
print(rasbNaSlag(a[0]))
b = Sym('2ab')
print(b.symbols)