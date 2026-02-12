from collections import defaultdict

def countSubarraysSum(A: list[int], K: int) -> int:
    """連続部分列の和がKになる個数を計算"""
    cnt = defaultdict(int)
    cnt[0] = 1
    s = 0
    result = 0
    for a in A:
        s += a
        result += cnt[s - K]
        cnt[s] += 1
    return result
