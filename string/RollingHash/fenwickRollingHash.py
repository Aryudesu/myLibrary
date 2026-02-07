from typing import Any, Tuple


class ModBit:
    """ACLのフェニ木をmod対応したもの"""
    def __init__(self, n: int = 0, mod: int = 998244353) -> None:
        self._n = n
        self._mod = mod
        self.data = [0] * n

    def add(self, p: int, x: Any) -> None:
        assert 0 <= p < self._n
        p += 1
        while p <= self._n:
            self.data[p - 1] = (self.data[p - 1] + x) % self._mod
            p += p & -p

    def sum(self, left: int, right: int) -> Any:
        assert 0 <= left <= right <= self._n
        return (self._sum(right) - self._sum(left)) % self._mod

    def _sum(self, r: int) -> Any:
        result = 0
        while r > 0:
            result = (result + self.data[r - 1]) % self._mod
            r -= r & -r
        return result

class FenwickRollingHash:
    """
    更新可能ダブルローリングハッシュ
    Edited By Aryu
    """
    def __init__(self, S: str|list[int], base1=37, MOD1=10**9 + 9, base2=157, MOD2 = 10**9 + 7):
        self.base1 = base1
        self.MOD1 = MOD1
        self.base2 = base2
        self.MOD2 = MOD2
        # 元データ
        self.N = len(S)
        # ハッシュ計算
        self.hash1 = []
        self.powData1 = []
        self.hash2 = []
        self.powData2 = []
        if isinstance(S, str):
            vals = [ord(c) for c in S]
        else:
            vals = list(S)
        self.vals = vals

        self.powData1 = [1] * (self.N + 1)
        self.powData2 = [1] * (self.N + 1)
        for i in range(self.N):
            self.powData1[i+1] = (self.powData1[i] * self.base1) % self.MOD1
            self.powData2[i+1] = (self.powData2[i] * self.base2) % self.MOD2
        self.invPowData1 = [1] * (self.N + 1)
        self.invPowData2 = [1] * (self.N + 1)
        invBase1 = pow(self.base1, self.MOD1-2, self.MOD1)
        invBase2 = pow(self.base2, self.MOD2-2, self.MOD2)
        for i in range(self.N):
            self.invPowData1[i+1] = (self.invPowData1[i] * invBase1) % self.MOD1
            self.invPowData2[i+1] = (self.invPowData2[i] * invBase2) % self.MOD2
        
        self.fenwick1 = ModBit(self.N, self.MOD1)
        self.fenwick2 = ModBit(self.N, self.MOD2)
        for i, v in enumerate(vals):
            self.fenwick1.add(i, v * self.powData1[i] % self.MOD1)
            self.fenwick2.add(i, v * self.powData2[i] % self.MOD2)


    def get(self, l: int, r: int)-> Tuple[int, int]:
        """[l, r)のハッシュ値を2つ返却"""
        assert 0 <= l <= r <= self.N
        res1 = self.fenwick1.sum(l, r) * self.invPowData1[l]
        res2 = self.fenwick2.sum(l, r) * self.invPowData2[l]
        return (res1 % self.MOD1, res2 % self.MOD2)

    def hashAll(self) -> Tuple[int, int]:
        """全体のハッシュ"""
        return self.get(0, self.N)

    def update(self, p: int, x: Any):
        """途中データの更新を行います"""
        assert 0 <= p < self.N
        if isinstance(x, str):
            assert len(x) == 1
            x = ord(x)
        old = self.vals[p]
        self.vals[p] = x
        d1 = ((x - old) * self.powData1[p]) % self.MOD1
        d2 = ((x - old) * self.powData2[p]) % self.MOD2
        self.fenwick1.add(p, d1)
        self.fenwick2.add(p, d2)

    def __len__(self)->int:
        return self.N


# === ABC331F
N, Q = map(int, input().split())
S = input()
SR = S[::-1]
sHash = FenwickRollingHash(S)
srHash = FenwickRollingHash(SR)
result = []
for _ in range(Q):
    n, a, b = input().split()
    if n == "1":
        x, c = int(a) - 1, b
        sHash.update(x, c)
        srHash.update(N - x + 1, c)
    elif n == "2":
        L, R = int(a) - 1, int(b) - 1
        if sHash.get(L, R + 1) == srHash.get(N - R - 1, N - L):
            result.append("Yes")
        else:
            result.append("No")
    else:
        raise Exception()
for r in result:
    print(r)
