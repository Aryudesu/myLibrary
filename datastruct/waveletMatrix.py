class BitVector:
    """0/1 ビット列に対して rank を高速に取る補助クラス"""
    w = 64

    def __init__(self, n: int):
        self.n = n
        self.blockSize = (n // self.w) + 1
        self.block = [0] * self.blockSize
        self.count = [0] * self.blockSize
        self.zeros = 0  # WaveletMatrix が設定する値

    def set(self, i: int) -> None:
        self.block[i // self.w] |= (1 << (i % self.w))

    def build(self) -> None:
        """rank 用の累積 1 個数 count[] を作る"""
        for i in range(1, self.blockSize):
            self.count[i] = self.count[i - 1] + self.block[i - 1].bit_count()

    def rank1(self, i: int) -> int:
        """[0, i) に含まれる 1 の数"""
        block_idx = i // self.w
        bit_index = i % self.w
        mask = (1 << bit_index) - 1
        return self.count[block_idx] + (self.block[block_idx] & mask).bit_count()

    def rank0(self, i: int) -> int:
        """[0, i) に含まれる 0 の数（rank1 を使わず独立計算 → 高速化）"""
        block_idx = i // self.w
        bit_index = i % self.w
        mask = (1 << bit_index) - 1
        ones = self.count[block_idx] + (self.block[block_idx] & mask).bit_count()
        return i - ones

    def get(self, i: int) -> int:
        return (self.block[i // self.w] >> (i % self.w)) & 1


class WaveletMatrix:
    """
    非負整数列に対する Wavelet Matrix
    ・index は 0-origin
    ・区間は [l, r)
    """

    def __init__(self, a: list[int] | int):
        if isinstance(a, int):
            # サイズだけ確保して、後で a を詰めて build() するモード
            self.n = a
            self.a = [0] * a
            self.lg = 0
            self.bv = []
        else:
            self.a = list(a)
            self.n = len(self.a)
            self.build()

    def build(self):
        if self.n == 0:
            self.lg = 0
            self.bv = []
            return

        maxVal = max(self.a)
        self.lg = max(maxVal.bit_length(), 1)
        self.bv = [BitVector(self.n) for _ in range(self.lg)]

        cur = self.a[:]
        nxt = [0] * self.n

        for h in range(self.lg - 1, -1, -1):
            bvh = self.bv[h]
            zeros = 0

            for i, v in enumerate(cur):
                if (v >> h) & 1:
                    bvh.set(i)
                else:
                    zeros += 1

            bvh.build()
            bvh.zeros = zeros

            p0, p1 = 0, zeros
            for v in cur:
                if (v >> h) & 1:
                    nxt[p1] = v
                    p1 += 1
                else:
                    nxt[p0] = v
                    p0 += 1

            cur, nxt = nxt, cur

    def rebuild(self):
        """サイズだけ指定したモードで、後から a を詰めたあとに呼ぶ。"""
        self.build()

    def access(self, k: int) -> int:
        """a[k]（0-index）の値を返す"""
        assert 0 <= k < self.n
        if self.lg == 0:
            return 0

        res = 0
        bv = self.bv

        for h in range(self.lg - 1, -1, -1):
            bvh = bv[h]
            if bvh.get(k):
                res |= (1 << h)
                k = bvh.rank1(k) + bvh.zeros
            else:
                k = bvh.rank0(k)

        return res

    def kthSmallest(self, l: int, r: int, k: int) -> int:
        """[l, r) で k 番目の最小値 (0-index)"""
        assert 0 <= l <= r <= self.n
        assert 0 <= k < r - l

        res = 0
        bv = self.bv

        for h in range(self.lg - 1, -1, -1):
            bvh = bv[h]
            rank0 = bvh.rank0
            zeros = bvh.zeros

            l0 = rank0(l)
            r0 = rank0(r)
            cnt0 = r0 - l0

            if k < cnt0:
                l, r = l0, r0
            else:
                k -= cnt0
                res |= (1 << h)
                l += zeros - l0
                r += zeros - r0

        return res

    def kthLargest(self, l: int, r: int, k: int) -> int:
        return self.kthSmallest(l, r, (r - l - 1) - k)

    def rangeFreq(self, l: int, r: int, upper: int) -> int:
        """[l, r) で x < upper の x の個数"""
        assert 0 <= l <= r <= self.n

        if self.lg == 0:
            return 0
        if upper <= 0:
            return 0
        if upper >= (1 << self.lg):
            return r - l

        cnt = 0
        bv = self.bv

        for h in range(self.lg - 1, -1, -1):
            f = (upper >> h) & 1
            bvh = bv[h]
            zeros = bvh.zeros
            rank0 = bvh.rank0

            l0 = rank0(l)
            r0 = rank0(r)

            if f:
                cnt += r0 - l0
                l += zeros - l0
                r += zeros - r0
            else:
                l, r = l0, r0

        return cnt

    def rangeFreqRange(self, l: int, r: int, lower: int, upper: int) -> int:
        return self.rangeFreq(l, r, upper) - self.rangeFreq(l, r, lower)

    def prevValue(self, l: int, r: int, upper: int) -> int:
        """upper 未満の最大値"""
        cnt = self.rangeFreq(l, r, upper)
        return -1 if cnt == 0 else self.kthSmallest(l, r, cnt - 1)

    def nextValue(self, l: int, r: int, lower: int) -> int:
        """lower 以上の最小値"""
        cnt = self.rangeFreq(l, r, lower)
        return -1 if cnt == r - l else self.kthSmallest(l, r, cnt)



wm = WaveletMatrix([3, 1, 4, 1, 5, 9, 2])
tmp = wm.kthSmallest(2, 5, 2)
print(tmp)
