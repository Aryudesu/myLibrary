from bisect import bisect_left, bisect_right
from collections import defaultdict


class OccurrenceIndex:
    """静的配列の値ごとの出現位置。0-index、半開区間 [l, r)。

    前処理・空間 O(N)。値は hashable。
    """

    def __init__(self, A):
        self.n = len(A)
        pos = defaultdict(list)
        for i, x in enumerate(A):
            pos[x].append(i)
        self._pos = {x: tuple(ids) for x, ids in pos.items()}

    def getPositions(self, x) -> tuple[int, ...]:
        """出現位置の変更不能な一覧。O(1) 平均。"""
        return self._pos.get(x, ())

    def _bounds(self, l, r, x):
        if not 0 <= l <= r <= self.n:
            raise ValueError("invalid interval")
        ids = self.getPositions(x)
        return ids, bisect_left(ids, l), bisect_left(ids, r)

    def count(self, l: int, r: int, x) -> int:
        ids, s, e = self._bounds(l, r, x)
        return e - s

    def prev(self, i: int, x) -> int:
        """i 未満の最後の出現位置。なければ -1。"""
        ids = self.getPositions(x)
        k = bisect_left(ids, i)
        return ids[k - 1] if k else -1

    def next(self, i: int, x) -> int:
        """i より後の最初の出現位置。なければ N。"""
        ids = self.getPositions(x)
        k = bisect_right(ids, i)
        return ids[k] if k < len(ids) else self.n

    def kth(self, l: int, r: int, x, k: int) -> int:
        """区間内の k 番目 (0-index)。存在しなければ -1。"""
        ids, s, e = self._bounds(l, r, x)
        return ids[s + k] if 0 <= k < e - s else -1

    def countExactK(self, l: int, r: int, x, k: int) -> int:
        """[l,r) 内で x をちょうど k 個含む非空部分区間数。

        O(log N + f) (f は区間内の x の出現回数)。
        """
        if k < 0:
            raise ValueError("k must be nonnegative")
        ids, s, e = self._bounds(l, r, x)
        if k > e - s:
            return 0
        if k == 0:
            result = 0
            prev = l - 1
            for i in range(s, e):
                gap = ids[i] - prev - 1
                result += gap * (gap + 1) // 2
                prev = ids[i]
            gap = r - prev - 1
            return result + gap * (gap + 1) // 2

        result = 0
        for i in range(s, e - k + 1):
            prev = ids[i - 1] if i > s else l - 1
            nxt = ids[i + k] if i + k < e else r
            result += (ids[i] - prev) * (nxt - ids[i + k - 1])
        return result
