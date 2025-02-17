def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y


# ABC340 - F
from math import gcd


def calc(X, Y):
    g = abs(gcd(X, Y))
    if g > 2:
        return None
    elif g == 2:
        X, Y = X // 2, Y // 2
    _, a, b = extended_gcd(X, Y)
    return -b * (3 - g), a * (3 - g)


X, Y = [int(l) for l in input().split()]
res = calc(X, Y)
if res is None:
    print(-1)
else:
    print(*res)
