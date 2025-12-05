class RangeConstAssignSumIter:
    """
    固定値 C の区間代入 + 区間和セグ木（非再帰）
    - assign(l, r): A[l:r] = C
    - sum(l, r):    A[l:r] の総和
    - point_set(i, v): A[i] = vを代入
    """
    __slots__ = ("n", "size", "log", "seg", "lazy_flag", "length", "C")

    def __init__(self, n: int, C: int, init: list[int] | None = None) -> None:
        self.n = n
        self.C = C
        size = 1
        log = 0
        while size < n:
            size <<= 1
            log += 1
        self.size = size
        self.log = log
        self.seg = [0] * (2 * size)
        self.lazy_flag = [False] * (2 * size)
        self.length = [0] * (2 * size)

        for k in range(size, 2 * size):
            self.length[k] = 1
        for k in range(size - 1, 0, -1):
            self.length[k] = self.length[k * 2] + self.length[k * 2 + 1]

        if init is not None:
            assert len(init) == n
            base = size
            seg = self.seg
            for i, v in enumerate(init):
                seg[base + i] = v
            for k in range(size - 1, 0, -1):
                seg[k] = seg[k * 2] + seg[k * 2 + 1]

    def _apply_const(self, k: int) -> None:
        """ノード k を全部 Cにする"""
        C = self.C
        self.seg[k] = C * self.length[k]
        self.lazy_flag[k] = True

    def _push_to_leaf(self, k: int) -> None:
        seg = self.seg
        lazy_flag = self.lazy_flag
        length = self.length
        C = self.C
        for h in range(self.log, 0, -1):
            p = k >> h
            if lazy_flag[p]:
                c1 = p << 1
                c2 = c1 | 1
                seg[c1] = C * length[c1]
                seg[c2] = C * length[c2]
                lazy_flag[c1] = True
                lazy_flag[c2] = True
                lazy_flag[p] = False

    def _recalc_from_leaf(self, k: int) -> None:
        seg = self.seg
        lazy_flag = self.lazy_flag
        k >>= 1
        while k:
            if not lazy_flag[k]:
                seg[k] = seg[k * 2] + seg[k * 2 + 1]
            k >>= 1

    def assign(self, l: int, r: int) -> None:
        """A[l:r] をCにする"""
        if l >= r:
            return
        size = self.size
        seg = self.seg
        lazy_flag = self.lazy_flag
        length = self.length
        C = self.C

        l += size
        r += size
        l0, r0 = l, r

        self._push_to_leaf(l0)
        self._push_to_leaf(r0 - 1)

        while l < r:
            if l & 1:
                seg[l] = C * length[l]
                lazy_flag[l] = True
                l += 1
            if r & 1:
                r -= 1
                seg[r] = C * length[r]
                lazy_flag[r] = True
            l >>= 1
            r >>= 1

        self._recalc_from_leaf(l0)
        self._recalc_from_leaf(r0 - 1)

    def sum(self, l: int, r: int) -> int:
        """A[l:r] の総和"""
        if l >= r:
            return 0
        size = self.size
        seg = self.seg

        l += size
        r += size

        self._push_to_leaf(l)
        self._push_to_leaf(r - 1)

        res = 0
        while l < r:
            if l & 1:
                res += seg[l]
                l += 1
            if r & 1:
                r -= 1
                res += seg[r]
            l >>= 1
            r >>= 1
        return res

    def point_set(self, i: int, v: int) -> None:
        """A[i] = vを代入"""
        size = self.size
        k = i + size
        self._push_to_leaf(k)
        self.seg[k] = v
        self.lazy_flag[k] = False
        self._recalc_from_leaf(k)

    def get(self, i: int) -> int:
        return self.sum(i, i + 1)
