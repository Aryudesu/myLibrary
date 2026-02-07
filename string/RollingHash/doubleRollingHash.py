from typing import Tuple

class RollingHash:
    """
    ダブルローリングハッシュライブラリ
    Edited by Aryu
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
        self.powData1 = [1] * (self.N + 1)
        self.hash1 = [0] * (self.N + 1)

        self.powData2 = [1] * (self.N + 1)
        self.hash2 = [0] * (self.N + 1)
        for i in range(self.N):
            self.powData1[i+1] = (self.powData1[i] * self.base1) % self.MOD1
            self.hash1[i+1] = (self.hash1[i] * self.base1 + vals[i]) % self.MOD1
            self.powData2[i+1] = (self.powData2[i] * self.base2) % self.MOD2
            self.hash2[i+1] = (self.hash2[i] * self.base2 + vals[i]) % self.MOD2
    
    def get(self, l: int, r: int)-> Tuple[int, int]:
        """[l, r)のハッシュ値を2つ返却"""
        assert 0 <= l <= r <= self.N
        res1 = self.hash1[r] - self.hash1[l] * self.powData1[r-l]
        res2 = self.hash2[r] - self.hash2[l] * self.powData2[r-l]
        return (res1 % self.MOD1, res2 % self.MOD2)

    def hashAll(self) -> Tuple[int, int]:
        """全体のハッシュ"""
        return (self.hash1[-1], self.hash2[-1])
    
    def find(self, pattern: "RollingHash")->int:
        """最初に出現する位置の探索を行います．"""
        if len(self) < len(pattern) or len(pattern) == 0:
            return -1
        target = pattern.hashAll()
        for idx in range(len(self) - len(pattern) + 1):
            if self.get(idx, idx + len(pattern)) == target:
                return idx
        return -1
    
    def findAll(self, pattern: "RollingHash")->list[int]:
        """出現する位置の探索を行います．"""
        if len(self) < len(pattern) or len(pattern) == 0:
            return []
        result = []
        target = pattern.hashAll()
        for idx in range(len(self) - len(pattern) + 1):
            if self.get(idx, idx + len(pattern)) == target:
                result.append(idx)
        return result
    
    def lcp(self, other: "RollingHash")->int:
        """最長共通接頭辞の長さを返却します．"""
        l = 0
        r = min(len(self), len(other)) + 1
        while r - l > 1:
            mid = (r + l) // 2
            if self.get(0, mid) == other.get(0, mid):
                l = mid
            else:
                r = mid
        return l

    def contains(self, pattern: "RollingHash")->bool:
        """包括確認を行います．"""
        return self.find(pattern) != -1
    
    def __contains__(self, pattern: "RollingHash")->bool:
        """包括確認を行います．"""
        return self.contains(pattern)

    def __len__(self):
        """代入された文字列長を返却します．"""
        return self.N


# ABC430E
result = []
T = int(input())
for _ in range(T):
    A = input()
    B = input()
    aHash = RollingHash(A + A)
    bHash = RollingHash(B)
    idx = aHash.find(bHash)
    result.append(idx)
for r in result:
    print(r)
