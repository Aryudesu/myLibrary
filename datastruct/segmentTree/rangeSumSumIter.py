import sys
sys.setrecursionlimit(1_000_000)
input = sys.stdin.readline


class RangeAddSumIter:
    """
    区間加算 + 区間和セグ木
    """
    __slots__ = ("n", "size", "log", "seg", "lazy", "length")

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
        self.lazy = [0] * (2 * size)
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

    def _apply(self, k: int, v: int) -> None:
        """ノード k に「区間全体に +v」の加算を適用"""
        self.seg[k] += v * self.length[k]
        self.lazy[k] += v

    def _push_to_leaf(self, k: int) -> None:
        """根からノード k までに溜まっている遅延をすべて子へ落とす"""
        seg = self.seg
        lazy = self.lazy
        length = self.length
        for h in range(self.log, 0, -1):
            p = k >> h
            if lazy[p] != 0:
                v = lazy[p]
                c1 = p << 1
                c2 = c1 | 1
                seg[c1] += v * length[c1]
                seg[c2] += v * length[c2]
                lazy[c1] += v
                lazy[c2] += v
                lazy[p] = 0

    def _recalc_from_leaf(self, k: int) -> None:
        """ノード k から根まで seg を再計算（lazy が 0 のところだけ）"""
        seg = self.seg
        lazy = self.lazy
        k >>= 1
        while k:
            if lazy[k] == 0:
                seg[k] = seg[k * 2] + seg[k * 2 + 1]
            k >>= 1

    def add(self, l: int, r: int, v: int) -> None:
        """A[l:r] に v を加算"""
        if l >= r:
            return
        size = self.size
        seg = self.seg
        lazy = self.lazy
        length = self.length

        l += size
        r += size
        l0, r0 = l, r

        self._push_to_leaf(l0)
        self._push_to_leaf(r0 - 1)

        while l < r:
            if l & 1:
                seg[l] += v * length[l]
                lazy[l] += v
                l += 1
            if r & 1:
                r -= 1
                seg[r] += v * length[r]
                lazy[r] += v
            l >>= 1
            r >>= 1

        self._recalc_from_leaf(l0)
        self._recalc_from_leaf(r0 - 1)

    def sum(self, l: int, r: int) -> int:
        """A[l:r] の総和を計算します"""
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

    def point_add(self, i: int, v: int) -> None:
        """A[i] に v を加算します"""
        self.add(i, i + 1, v)

    def get(self, i: int) -> int:
        """A[i] を返却します"""
        return self.sum(i, i + 1)


# === AWC0013E

N, Q = map(int, input().split())
C = list(map(int, input().split()))
st = RangeAddSumIter(N, C)
result = []
for _ in range(Q):
    n, *query = list(map(int, input().split()))
    if n == 1:
        l, r, v = query
        st.add(l-1, r, v)
    elif n == 2:
        l, r = query
        result.append(st.sum(l-1, r))
    else:
        raise ValueError()
for r in result:
    print(r)

