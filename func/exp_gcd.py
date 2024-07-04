import math


def ext_gcd(a, b, x, y):
    """拡張ユークリッドの互除法"""
    if b == 0:
        x[0] = 1
        y[0] = 0
        return a
    d = ext_gcd(b, a % b, y, x)
    y[0] -= (a // b) * x[0]
    return d

def calc(X, Y):
    m = -10**18
    M = 10**18
    g = abs(math.gcd(X, Y))
    if g > 2:
        return None
    if g == 2:
        X, Y = X // 2, Y // 2
    x, y = [0], [0]
    ext_gcd(X, Y, x, y)
    a, b = x[0], y[0]
    if m <= a and a <= M and m <= b and b <= M:
        pass
    else:
        return None
    for i in range(2):
        for j in range(2):
            if a * X * (i * 2 - 1) + b * Y * (j * 2 - 1) == 1:
                if g == 1:
                    return (-b * (j * 2 - 1) * 2, a * (i * 2 - 1) * 2)
                else:
                    return (-b * (j * 2 - 1), a * (i * 2 - 1))
    return None

# *** Example (ABC340 F) ***
X, Y = [int(l) for l in input().split()]
res = calc(X, Y)
if res is None:
    print(-1)
else:
    print(*res)
