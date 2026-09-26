from collections.abc import Sequence


class RangeAddRangeSum:
    """
    区間加算 + 区間和取得を行う遅延セグメント木。

    区間はすべて半開区間 [l, r) とする。

    RangeAddRangeSum(n):
        長さ n、全要素 0 で初期化。

    RangeAddRangeSum(A):
        配列 A で初期化。

    range_add(l, r, x):
        A[l:r] の全要素に x を加算。

    range_sum(l, r):
        sum(A[l:r]) を返す。

    計算量:
        構築 O(N)
        range_add / range_sum O(log N)
    """

    def __init__(self, data: int | Sequence[int]):
        if isinstance(data, int):
            assert data >= 0
            self.n = data
            values = [0] * data
        else:
            values = list(data)
            self.n = len(values)

        self.size = 1
        while self.size < self.n:
            self.size <<= 1

        self.sum_data = [0] * (2 * self.size)
        self.lazy = [0] * (2 * self.size)
        self.length = [0] * (2 * self.size)

        for i in range(self.size):
            self.length[self.size + i] = 1 if i < self.n else 0

        for k in range(self.size - 1, 0, -1):
            self.length[k] = self.length[k << 1] + self.length[k << 1 | 1]

        for i, x in enumerate(values):
            self.sum_data[self.size + i] = x

        for k in range(self.size - 1, 0, -1):
            self._pull(k)

    def _pull(self, k: int) -> None:
        self.sum_data[k] = self.sum_data[k << 1] + self.sum_data[k << 1 | 1]

    def _apply(self, k: int, x: int) -> None:
        self.sum_data[k] += x * self.length[k]
        self.lazy[k] += x

    def _push(self, k: int) -> None:
        x = self.lazy[k]
        if x == 0:
            return

        self._apply(k << 1, x)
        self._apply(k << 1 | 1, x)
        self.lazy[k] = 0

    def range_add(self, l: int, r: int, x: int) -> None:
        """[l, r) の全要素に x を加算する。"""
        assert 0 <= l <= r <= self.n
        if l == r:
            return

        self._range_add(l, r, x, 1, 0, self.size)

    def _range_add(
        self,
        l: int,
        r: int,
        x: int,
        k: int,
        nl: int,
        nr: int,
    ) -> None:
        if nr <= l or r <= nl:
            return

        if l <= nl and nr <= r:
            self._apply(k, x)
            return

        self._push(k)
        mid = (nl + nr) >> 1
        self._range_add(l, r, x, k << 1, nl, mid)
        self._range_add(l, r, x, k << 1 | 1, mid, nr)
        self._pull(k)

    def range_sum(self, l: int, r: int) -> int:
        """sum(A[l:r]) を返す。"""
        assert 0 <= l <= r <= self.n
        if l == r:
            return 0

        return self._range_sum(l, r, 1, 0, self.size)

    def _range_sum(
        self,
        l: int,
        r: int,
        k: int,
        nl: int,
        nr: int,
    ) -> int:
        if nr <= l or r <= nl:
            return 0

        if l <= nl and nr <= r:
            return self.sum_data[k]

        self._push(k)
        mid = (nl + nr) >> 1
        return (
            self._range_sum(l, r, k << 1, nl, mid)
            + self._range_sum(l, r, k << 1 | 1, mid, nr)
        )

    def all_sum(self) -> int:
        """配列全体の総和を返す。"""
        return self.sum_data[1]

    def get(self, i: int) -> int:
        """A[i] を返す。"""
        assert 0 <= i < self.n
        return self.range_sum(i, i + 1)

    def __getitem__(self, i: int) -> int:
        return self.get(i)

    def __len__(self) -> int:
        return self.n
