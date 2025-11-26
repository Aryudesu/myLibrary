class BitVector:
    w = 64

    def __init__(self, n: int):
        self.n = n
        self.zeros = n
        self.blockSize = (n//self.w) + 1
        self.block = [0] * self.blockSize
        self.count = [0] * self.blockSize

    def build(self):
        for i in range(1, self.blockSize):
            self.count[i] = self.count[i-1] + self.block[i-1].bit_count()
        self.zeros = self.rank0(self.n)
    
    def rank0(self, i: int) -> int:
        bit_index = i % self.w
        mask = (1 << bit_index) - 1
        low_bits = self.block[i//self.w] & mask
        rank1 = self.count[i//self.w] + low_bits.bit_count()
        return i - rank1
    
    def get(self, i: int)-> int:
        return (self.block[i//self.w] >> (i%self.w)) & 1
    
    def set(self, i: int):
        self.block[i//self.w] |= (1 << (i%self.w))

class WaveletMatrix:
    def __init__(self, a: list[int] | int):
        self.bv: list[BitVector] = []
        if isinstance(a, int):
            self.n = max(a, 1)
            self.a = [0] * self.n
        else:
            self.a = list(a)
            self.n = len(self.a)
            self.build()

    def build(self):
        maxVal = max(max(self.a) if self.a else 0, 1)
        self.lg = maxVal.bit_length()
        self.bv = [BitVector(self.n) for _ in range(self.lg)]

        cur = self.a[:]
        nxt = [0] * self.n
        n = self.n

        for h in range(self.lg - 1, -1, -1):
            bvh = self.bv[h]
            zeros = 0
            for i in range(n):
                v = cur[i]
                bit = (v >> h) & 1
                if bit:
                    bvh.set(i)
                else:
                    zeros += 1
            bvh.build()
            bvh.zeros = zeros  
            p0 = 0
            p1 = zeros
            for i in range(n):
                v = cur[i]
                if (v >> h) & 1:
                    nxt[p1] = v
                    p1 += 1
                else:
                    nxt[p0] = v
                    p0 += 1
            cur, nxt = nxt, cur
    
    def set(self, i: int, x):
        assert x >= 0
        self.a[i] = x
    
    def access(self, k: int):
        """k番目の要素の値"""
        ret = 0
        for h in range(self.lg - 1, -1, -1):
            f = self.bv[h].get(k)
            ret |= ((1 << h) if f != 0 else 0)
            k = (self.bv[h].rank1(k) + self.bv[h].zeros) if f != 0 else self.bv[h].rank0(k)
        return ret

    def kthSmallest(self, l: int, r: int, k: int):
        """[l, r)の範囲でk番目に小さい値"""
        res = 0
        bv = self.bv
        for h in range(self.lg - 1, -1, -1):
            bvh: BitVector = bv[h]
            rank0 = bvh.rank0
            zeros = bvh.zeros
            l0: int = rank0(l)
            r0: int = rank0(r)
            if k < r0 - l0:
                l = l0
                r = r0
            else:
                k -= r0 - l0
                res |= (1 << h)
                l += zeros - l0
                r += zeros - r0
        return res
    
    def kthLargest(self, l: int, r: int, k: int):
        """[l, r)の範囲でk番目に大きい値"""
        return self.kthSmallest(l, r, r - l - k - 1)
    
    def rangeFreq(self, l: int, r: int, upper):
        """[l, r)の範囲でupper未満の値の個数"""
        if upper >= (1 << self.lg):
            return r - l
        ret = 0
        bv = self.bv
        for h in range(self.lg - 1, -1, -1):
            bvh: BitVector = bv[h]
            rank0 = bvh.rank0
            zeros = bvh.zeros
            f = (upper >> h) & 1
            l0: int = rank0(l)
            r0: int = rank0(r)
            if f != 0:
                ret += r0 - l0
                l += zeros - l0
                r += zeros - r0
            else:
                l = l0
                r = r0
        return ret
    
    def rangeFreqRange(self, l: int, r: int, lower, upper):
        return self.rangeFreq(l, r, upper) - self.rangeFreq(l, r, lower)
    
    def prevValue(self, l: int, r: int, upper):
        """l, rの範囲でupper未満の最後の値"""
        cnt: int = self.rangeFreq(l, r, upper)
        return -1 if cnt == 0 else self.kthSmallest(l, r, cnt - 1)
    
    def nextValue(self, l: int, r: int, lower):
        """l, rの範囲でlower以上の最初の値"""
        cnt: int = self.rangeFreq(l, r, lower)
        return -1 if cnt == r - l else self.kthSmallest(l, r, cnt)


wm = WaveletMatrix([3, 1, 4, 1, 5, 9, 2])
tmp = wm.kthSmallest(2, 5, 2)
print(tmp)
