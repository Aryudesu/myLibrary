class FirstGE:
    """最初に value >= x を満たす位置を探すセグ木"""
    def __init__(self, A):
        n = len(A)
        size = 1
        while size < n:
            size <<= 1

        self.n = n
        self.size = size
        self.seg = [-1] * (2 * size)

        for i in range(n):
            self.seg[size + i] = A[i]

        for i in range(size - 1, 0, -1):
            self.seg[i] = max(self.seg[i << 1], self.seg[i << 1 | 1])

    def find_first(self, x):
        """value >= x を満たす最小 index"""
        if self.seg[1] < x:
            return -1

        k = 1
        while k < self.size:
            if self.seg[k << 1] >= x:
                k <<= 1
            else:
                k = k << 1 | 1

        return k - self.size

    def erase(self, i):
        """位置 i を使用済みにする"""
        k = i + self.size
        self.seg[k] = -1

        k >>= 1
        while k:
            self.seg[k] = max(self.seg[k << 1], self.seg[k << 1 | 1])
            k >>= 1
