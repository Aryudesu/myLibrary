def weightedDistanceSum1D(W: list[int]) -> list[int]:
    """
    1次元上の各位置 x について、重み付き距離和
        sum(W[i] * abs(i - x))
    を求める。

    Args:
        W:
            index i に置かれた重み W[i]。
            負の重みでも計算自体は可能。

    Returns:
        result[x] = sum(W[i] * abs(i - x))

    計算量:
        O(N)

    Note:
        x から x+1 に移動したとき、
        左側の重みぶん距離が増え、右側の重みぶん距離が減ることを利用する。
    """
    N = len(W)

    if N == 0:
        return []

    total = sum(W)
    cur = sum(i * w for i, w in enumerate(W))

    result = [cur]
    left = 0

    for x in range(N - 1):
        left += W[x]
        cur += 2 * left - total
        result.append(cur)

    return result
