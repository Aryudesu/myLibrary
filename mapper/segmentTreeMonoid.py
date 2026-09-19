from typing import TypeAlias

Number: TypeAlias = int | float
MinMaxNode: TypeAlias = tuple[Number, Number]

MIN_MAX_E: MinMaxNode = (float("inf"), float("-inf"))


def minMaxOp(a: MinMaxNode, b: MinMaxNode) -> MinMaxNode:
    """
    ACL SegTree で区間最小値・最大値を同時に管理するための二項演算。

    Args:
        a, b:
            (区間最小値, 区間最大値)

    Returns:
        a, b を結合した区間の (最小値, 最大値)

    Example:
        from atcoder.segtree import SegTree

        A = [3, 1, 4, 2]
        st = SegTree(
            minMaxOp,
            MIN_MAX_E,
            [(x, x) for x in A],
        )

        # [1, 4) の min / max
        minValue, maxValue = st.prod(1, 4)
        # (1, 4)
    """
    return min(a[0], b[0]), max(a[1], b[1])


def minMaxNode(x: int) -> MinMaxNode:
    """値 x を min/max SegTree 用の葉ノード (x, x) に変換する。"""
    return x, x


def minMaxNodes(A: list[int]) -> list[MinMaxNode]:
    """配列 A を min/max SegTree 用の葉ノード列に変換する。"""
    return [minMaxNode(x) for x in A]
