def hilbertOrder(x: int, y: int, bits: int) -> int:
    """
    2^bits x 2^bits 上の (x, y) の Hilbert order を返す。

    再帰を使わない反復実装。
    Mo's Algorithm のクエリ順序付けに利用できる。
    """
    n = 1 << bits
    d = 0
    s = n >> 1

    while s:
        rx = 1 if x & s else 0
        ry = 1 if y & s else 0

        d += s * s * ((3 * rx) ^ ry)

        if ry == 0:
            if rx == 1:
                x = n - 1 - x
                y = n - 1 - y
            x, y = y, x

        s >>= 1

    return d


def sortMoQueriesHilbert(
    queries: list[tuple[int, int, int, int]],
    maxCoord: int,
) -> list[tuple[int, int, int, int]]:
    """
    TreeMoInline の (l, r, lca, queryIndex) を Hilbert order で並べる。

    Args:
        queries:
            (l, r, lca, queryIndex) のリスト。
        maxCoord:
            座標の上限。TreeMoInline なら len(tm.euler) を渡す。

    Returns:
        Hilbert order 順に並べたクエリ。

    計算量:
        Hilbert index 計算 O(Q log(maxCoord))
        ソート O(Q log Q)

    Example:
        tm = TreeMoInline(graph)
        ...
        ordered = sortMoQueriesHilbert(tm.queries, len(tm.euler))
    """
    if not queries:
        return []

    bits = max(1, maxCoord.bit_length())

    decorated = [
        (hilbertOrder(l, r, bits), l, r, w, qi)
        for l, r, w, qi in queries
    ]
    decorated.sort(key=lambda x: x[0])

    return [(l, r, w, qi) for _, l, r, w, qi in decorated]
