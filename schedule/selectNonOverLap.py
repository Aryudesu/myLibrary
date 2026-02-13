from typing import Iterable, Tuple

def maxNonOverlappingIntervals(intervals: Iterable[Tuple[int, int]])-> int:
    """[l, r)の区間列挙"""
    LR: list[Tuple[int, int]] = sorted(intervals, key = lambda x: x[1])
    cur = -10 ** 30
    result = []
    for l, r in LR:
        if l >= cur:
            result.append((l, r))
            cur = r
    return result
