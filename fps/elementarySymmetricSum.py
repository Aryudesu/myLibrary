def elementary_symmetric_sum(values: list[int], K: int, mod: int) -> list[int]:
    """
    prod(1 + values[i] * x) の x^0 ～ x^K の係数を返す。
    """
    dp = [0] * (K + 1)
    dp[0] = 1

    for i, value in enumerate(values, 1):
        for k in range(min(i, K), 0, -1):
            dp[k] = (dp[k] + dp[k - 1] * value) % mod

    return dp


