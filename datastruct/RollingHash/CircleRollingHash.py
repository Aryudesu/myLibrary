class RollingHash:
    """ローリングハッシュライブラリ"""
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


class CircleRollingHash:
    """円環式ローリングハッシュライブラリ"""
    def __init__(self, S: str|list[int], base=37, MOD=10**9 + 9):
        self.base = base
        self.MOD = MOD
        # 元データ
        self.S = []
        if isinstance(S, str):
            self.S = [ord(s) for s in S]
        else:
            self.S = list(S)
        SS = self.S + self.S
        self.N = len(S)
        # ハッシュ計算
        self.rh = RollingHash(SS, base=base, MOD=MOD)
        self.offset = 0
    
    def shiftL(self, num: int = 1):
        """左方向にシフトを行います"""
        if num == 0:
            return
        self.offset = (self.offset + num) % self.N

    def shiftR(self, num: int = 1):
        """右方向にシフトを行います"""
        if num == 0:
            return
        self.offset = (self.offset - num) % self.N
    
    def getHashData(self)->int:
        """ハッシュ値を計算します"""
        return self.rh.get(self.offset, self.offset + self.N)

    def __eq__(self, value: "CircleRollingHash")->bool:
        if self.N != value.N:
            return False
        return self.getHashData() == value.getHashData()

result = []
T = int(input())
for t in range(T):
    A = input()
    B = input()
    a_hash = CircleRollingHash(A)
    b_hash = CircleRollingHash(B)
    if a_hash == b_hash:
        result.append(0)
        continue
    count = 0
    f = False
    for a in A:
        count += 1
        a_hash.shiftL()
        if a_hash == b_hash:
            f = True
            break
    if f:
        result.append(count)
    else:
        result.append(-1)
for r in result:
    print(r)

