from bisect import bisect_left, bisect_right
from atcoder.segtree import SegTree


class ZigzagDP:
    """
    増減が交互になる重み付き部分列の最大得点を管理する。
    A: 追加予定の整数値の集合（順序・重複は任意）。
    L, R: 隣接する選択値の差の絶対値の下限・上限。
    L=0 でも等値は増減に含めない。R=None でも上限なし。
    空部分列を許し、得点は0とする。負の重みも可。
    構築 O(M log M)（入力長M）、add O(log K)、getMax O(1)。
    Kは異なる値の個数。空間 O(K)。
    """

    def __init__(self, A, L=1, R=float("inf")):
        if R is None:
            R = float("inf")
        if L < 0 or R < L:
            raise ValueError("require 0 <= L <= R")
        self.A = sorted(set(A))
        self.ids = {a: i for i, a in enumerate(self.A)}
        self.L = max(1, L)
        self.R = R
        self.up = SegTree(max, float("-inf"), len(self.A))
        self.down = SegTree(max, float("-inf"), len(self.A))
        self.best = 0

    def add(self, a, b=1):
        """末尾に値a、重みbを追加する。aは構築時に登録済みとする。"""
        i = self.ids[a]
        A, L, R = self.A, self.L, self.R
        up = down = b
        if L <= R:
            ll = 0 if R == float("inf") else bisect_left(A, a - R)
            lr = bisect_right(A, a - L)
            rl = bisect_left(A, a + L)
            rr = len(A) if R == float("inf") else bisect_right(A, a + R)
            up += max(0, self.down.prod(ll, lr))
            down += max(0, self.up.prod(rl, rr))

        self.up.set(i, max(self.up.get(i), up))
        self.down.set(i, max(self.down.get(i), down))
        self.best = max(self.best, up, down)

    def getMax(self):
        """これまでに追加された要素の最大得点（空部分列を含む）。"""
        return self.best
