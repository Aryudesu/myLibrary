from typing import Iterable, Tuple

def maxNonOverlappingIntervals(intervals: Iterable[Tuple[int, int]])-> int:
    """[l, r)の区間列挙"""
    LR: list[Tuple[int, int]] = sorted(intervals, key = lambda x: x[1])
    cur = -10 ** 30
    result = 0
    for l, r in LR:
        if l >= cur:
            result += 1
            cur = r
    return result
