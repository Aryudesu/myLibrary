from heapq import heappop, heappush
from typing import Iterable, Tuple

def canAssignIntervalsToPoints(N: int, intervals: Iterable[Tuple[int, int]])-> bool:
    """
    intervalsに含まれる各区間[l, r]のうち1点を選び1..Nの点を重複無く選ぶことができるか判定
    """
    LR: list[Tuple[int, int]] = sorted(intervals)
    M = len(LR)
    if N < M or M == 0:
        return False
    data = []
    idx = 0
    for i in range(1, N + 1):
        while idx < M and LR[idx][0] <= i:
            heappush(data, LR[idx][1])
            idx += 1
        if len(data) == 0:
            continue
        r = heappop(data)
        if r < i:
            return False
    return idx == M and len(data) == 0
