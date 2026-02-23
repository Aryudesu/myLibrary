from typing import Tuple

def mergeIntervals(data: list[Tuple[int, int]])-> list[Tuple[int, int]]:
    """半開区間[L, R)の範囲結合を行います．"""
    if len(data) == 0:
        return []
    data.sort()
    result = [data[0]]
    for l, r in data[1:]:
        pl, pr = result[-1]
        if l <= pr:
            result[-1] = (pl, max(pr, r))
        else:
            result.append((l, r))
    return result

N, M = map(int, input().split())
LR = []
for m in range(M):
    l, r = map(int, input().split())
    LR.append((l, r+1))
interval = mergeIntervals(LR)
num = 0
prev = 1
n = 0
for l, r in interval:
    n = l - prev
    if num + n < N:
        num += n
    else:
        break
    prev = r
print(prev + N - num - 1)
