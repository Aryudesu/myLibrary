from bisect import bisect_left


def lisLength(A: list[int]) -> int:
    """LISの長さのみを計算するO(N log N)"""
    dp = []
    for a in A:
        i = bisect_left(dp, a)
        if i == len(dp):
            dp.append(a)
        else:
            dp[i] = a
    return len(dp)
