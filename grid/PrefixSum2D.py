class PrefixSum2D:
    def __init__(self, H: int, W: int):
        self.H = H
        self.W = W
        # 元データ
        self.orig = [[0] * W for _ in range(H)]
        self.sums = [[0] * W for _ in range(H)]
        self.initialized = False
    
    def add(self, h: int, w: int, x: int)-> None:
        """(h, w)にxを加算します"""
        assert not self.initialized
        if 0 <= h < self.H and 0 <= w < self.W:
            self.orig[h][w] += x
    
    def set(self, h: int, w: int, x: int)-> None:
        """(h, w)にxを設定します"""
        assert not self.initialized
        if 0 <= h < self.H and 0 <= w < self.W:
            self.orig[h][w] = x
    
    def build(self)-> None:
        """2次元累積和の計算を行います"""
        assert not self.initialized
        for h in range(self.H):
            s = 0
            for w in range(self.W):
                s += self.orig[h][w]
                self.sums[h + 1][w + 1] = s + self.sums[h][w + 1]
        self.initialized = True
    
    def sum(self, u: int, l: int, d: int, r: int)-> int:
        assert not self.initialized
        assert 0 <= u <= d < self.H
        assert 0 <= l <= r < self.W
        u1, l1, d1, r1 = u, l, d + 1, r + 1
        return self.sums[d1][r1] - self.sums[u1][r1] - self.sums[d1][l1] + self.sums[u1][l1]

    def getData(self)-> list[list[int]]:
        """元データを返却します"""
        return self.orig
    
    @staticmethod
    def makeData(cls, grid: list[list[int]])-> "PrefixSum2D":
        """
        既存の2次元グリッドから累積和を構築します
        """
        H = len(grid)
        W = len(grid[0]) if H > 0 else 0
        obj: "PrefixSum2D" = cls(H, W)
        for h in range(H):
            for w in range(W):
                obj.orig[h][w] = grid[h][w]
        obj.build()
        return obj


