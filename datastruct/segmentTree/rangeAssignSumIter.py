import sys
sys.setrecursionlimit(1_000_000)
input = sys.stdin.readline

class RangeAssignSumIter:
    """
    任意値の区間代入 + 区間和セグ木（非再帰・PyPy向け）

    - assign(l, r, v): A[l:r] = v
    - sum(l, r):       A[l:r] の総和
    - point_set(i, v): A[i] = v
    - get(i):          A[i] を取得
    """
    __slots__ = ("n", "size", "log", "seg", "lazy_flag", "lazy_val", "length")

    def __init__(self, n: int, init: list[int] | None = None) -> None:
        self.n = n
        size = 1
        log = 0
        while size < n:
            size <<= 1
            log += 1
        self.size = size
        self.log = log
        self.seg = [0] * (2 * size)
        self.lazy_flag = [False] * (2 * size)
        self.lazy_val = [0] * (2 * size)
        self.length = [0] * (2 * size)

        # 区間長（セグ木の1ノードが何要素分担当するか）
        for k in range(size, 2 * size):
            self.length[k] = 1
        for k in range(size - 1, 0, -1):
            self.length[k] = self.length[k * 2] + self.length[k * 2 + 1]

        if init is not None:
            assert len(init) == n
            # 葉に初期値をセット
            base = size
            seg = self.seg
            for i, v in enumerate(init):
                seg[base + i] = v
            # 残りの葉は 0 のまま
            for k in range(size - 1, 0, -1):
                seg[k] = seg[k * 2] + seg[k * 2 + 1]

    def _apply(self, k: int, v: int) -> None:
        """ノード k に「区間全部 v」の代入を適用"""
        self.seg[k] = v * self.length[k]
        self.lazy_flag[k] = True
        self.lazy_val[k] = v

    def _push_to_leaf(self, k: int) -> None:
        """根からノード k までの lazy をすべて子に落とす"""
        seg = self.seg
        lazy_flag = self.lazy_flag
        lazy_val = self.lazy_val
        length = self.length
        for h in range(self.log, 0, -1):
            p = k >> h
            if lazy_flag[p]:
                v = lazy_val[p]
                c1 = p << 1
                c2 = c1 | 1
                seg[c1] = v * length[c1]
                seg[c2] = v * length[c2]
                lazy_flag[c1] = True
                lazy_flag[c2] = True
                lazy_val[c1] = v
                lazy_val[c2] = v
                lazy_flag[p] = False

    def _recalc_from_leaf(self, k: int) -> None:
        """ノード k から根まで seg を再計算"""
        seg = self.seg
        lazy_flag = self.lazy_flag
        k >>= 1
        while k:
            if not lazy_flag[k]:
                seg[k] = seg[k * 2] + seg[k * 2 + 1]
            k >>= 1

    def assign(self, l: int, r: int, v: int) -> None:
        """A[l:r] を v で埋める"""
        if l >= r:
            return
        size = self.size
        seg = self.seg
        lazy_flag = self.lazy_flag
        lazy_val = self.lazy_val
        length = self.length

        l += size
        r += size
        l0, r0 = l, r

        self._push_to_leaf(l0)
        self._push_to_leaf(r0 - 1)

        while l < r:
            if l & 1:
                seg[l] = v * length[l]
                lazy_flag[l] = True
                lazy_val[l] = v
                l += 1
            if r & 1:
                r -= 1
                seg[r] = v * length[r]
                lazy_flag[r] = True
                lazy_val[r] = v
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
        """A[i] = v"""
        size = self.size
        k = i + size
        self._push_to_leaf(k)
        self._apply(k, v)
        self._recalc_from_leaf(k)

    def get(self, i: int) -> int:
        """A[i] を返す"""
        return self.sum(i, i + 1)
