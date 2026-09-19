from collections.abc import Iterator


def dyadicDecompose(L: int, R: int) -> Iterator[tuple[int, int]]:
    """
    半開区間 [L, R) を、開始位置が長さの倍数である 2 冪長区間に分解する。

    Args:
        L:
            区間の左端。
        R:
            区間の右端。R 自体は含まない。

    Yields:
        (l, length)
            区間 [l, l + length)。
            length は 2 の冪で、l % length == 0 を満たす。

    計算量:
        生成される区間数に比例。
        通常 O(log(R - L) + log R) 個程度。

    Example:
        [7, 19) ->
            [7, 8)
            [8, 16)
            [16, 18)
            [18, 19)

        返り値:
            (7, 1), (8, 8), (16, 2), (18, 1)

    Note:
        bit DP、popcount、巨大整数区間などで、
        2 冪境界に揃った区間へ分割したい場合に利用する。
    """
    assert 0 <= L <= R

    while L < R:
        rest = R - L
        maxLengthByRest = 1 << (rest.bit_length() - 1)

        if L == 0:
            length = maxLengthByRest
        else:
            length = min(L & -L, maxLengthByRest)

        yield L, length
        L += length
