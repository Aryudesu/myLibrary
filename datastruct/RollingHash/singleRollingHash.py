class SingleRollingHash:
    """単体ローリングハッシュライブラリ"""
    def __init__(self, S: str|list[int], base=37, MOD=10**9 + 9):
        self.base = base
        self.MOD = MOD
        # 元データ
        self.N = len(S)
        # ハッシュ計算
        self.hash = []
        self.powData = []
        if isinstance(S, str):
            vals = [ord(c) for c in S]
        else:
            vals = list(S)
        self.powData = [1] * (self.N + 1)
        self.hash = [0] * (self.N + 1)
        for i in range(self.N):
            self.powData[i+1] = (self.powData[i] * self.base) % self.MOD
            self.hash[i+1] = (self.hash[i] * self.base + vals[i]) % self.MOD
    
    def get(self, l: int, r: int)-> int:
        """[l, r)のハッシュ値を返却"""
        assert l >= 0
        assert r <= self.N
        assert l < r
        res = self.hash[r] - self.hash[l] * self.powData[r-l]
        return res % self.MOD
    
    def __len__(self):
        return self.N