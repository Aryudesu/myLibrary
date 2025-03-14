from atcoder.fenwicktree import FenwickTree
from sortedcontainers import SortedSet


def inversion_count(arr: list) -> int:
    result = 0
    ft = FenwickTree(max(arr) + 1)
    for i, a in enumerate(A):
        result += i - ft.sum(0, a + 1)
        ft.add(a, 1)
    return result


N, M = [int(l) for l in input().split()]
A = [int(l) for l in input().split()]
origin = inversion_count(A)

data = SortedSet()
for idx in range(N):
    a = A[idx]
    tmp = M - A[idx]
    data.add((tmp, idx))
result = []
for m in range(M):
    while True:
        if len(data) == 0:
            break
        num, idx = data.pop(0)
        if num > m:
            data.add((num, idx))
            break
        else:
            origin = origin - (N - idx - 1) + idx
    result.append(origin)
for r in result:
    print(r)
