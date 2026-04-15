class PrefixSum2D:
    """0-indexed座標のグリッドに対する2次元累積和"""
    def __init__(self, H: int, W: int):
        self.H = H
        self.W = W
        # 元データ
        self.orig = [[0] * W for _ in range(H)]
        self.sums = [[0] * (W + 1) for _ in range(H + 1)]
        self.initialized = False
    
    def add(self, h: int, w: int, x: int) -> None:
        """(h, w)にxを加算します"""
        assert not self.initialized
        if 0 <= h < self.H and 0 <= w < self.W:
            self.orig[h][w] += x
    
    def set(self, h: int, w: int, x: int) -> None:
        """(h, w)にxを設定します"""
        assert not self.initialized
        if 0 <= h < self.H and 0 <= w < self.W:
            self.orig[h][w] = x
    
    def build(self) -> None:
        """2次元累積和の計算を行います"""
        assert not self.initialized
        for h in range(self.H):
            s = 0
            for w in range(self.W):
                s += self.orig[h][w]
                self.sums[h + 1][w + 1] = s + self.sums[h][w + 1]
        self.initialized = True
    
    def sum(self, u: int, l: int, d: int, r: int) -> int:
        """矩形 [u, d] * [l, r] の総和を返します"""
        assert self.initialized
        assert 0 <= u <= d < self.H
        assert 0 <= l <= r < self.W
        u1, l1, d1, r1 = u, l, d + 1, r + 1
        return self.sums[d1][r1] - self.sums[u1][r1] - self.sums[d1][l1] + self.sums[u1][l1]

    def getData(self) -> list[list[int]]:
        """元データを返却します"""
        return self.orig

    def getSumTable(self) -> list[list[int]]:
        """累積和テーブル（1-indexed）を返却します"""
        assert self.initialized
        return self.sums
    
    @classmethod
    def makeData(cls, grid: list[list[int]]) -> "PrefixSum2D":
        """
        既存の2次元グリッドから累積和を構築します
        """
        H = len(grid)
        W = len(grid[0]) if H > 0 else 0
        obj = cls(H, W)
        for h in range(H):
            for w in range(W):
                obj.orig[h][w] = grid[h][w]
        obj.build()
        return obj

N, M, K = map(int, input().split())
psd = PrefixSum2D(N+1, M+1)
for n in range(N):
    S = input()
    for m in range(M):
        psd.add(n, m, int(S[m]))
psd.build()
result = -1
for h1 in range(N):
    for w1 in range(M):
        for h2 in range(h1, N):
            for w2 in range(w1, M):
                if (h2 - h1 + 1) * (w2 - w1 + 1) == K:
                    result = max(result, psd.sum(h1, w1, h2, w2))
print(result)

