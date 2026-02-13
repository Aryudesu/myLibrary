from typing import Callable

def binarySearchMaxTrue(left: int, right: int, isOk: Callable[[int], bool])->int:
    """left～rightの内isOkがtrueになる境界の探索"""
    l = left
    r = right
    while r - l > 1:
        m = (r + l) // 2
        if isOk(m):
            l = m
        else:
            r = m
    return l

# === AWC0005D
N, K = map(int, input().split())
A = list(map(int, input().split()))

def checkFunc(mid: int)->bool:
    """midが条件を満たすか"""
    s, c = 0, 0
    for a in A:
        s += a
        if s >= mid:
            s = 0
            c += 1
            if c >= K:
                return True
    return False

res = binarySearchMaxTrue(-1, sum(A) + 1, checkFunc)
print(res)
