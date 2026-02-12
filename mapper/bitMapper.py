from typing import Tuple, Iterator

class BitMapper:
    def __init__(self, n: int):
        self.n = n
        self.full = (1 << n) - 1

    def full_mask(self)->int:
        """マスク全体のデータ"""
        return self.full

    def toTuple(self, mask: int)-> Tuple[int, ...]:
        """タプルに変換します"""
        mask &= self.full
        result = []
        for _ in range(self.n):
            result.append(mask&1)
            mask>>=1
        result.reverse()
        return tuple(result)

    def subMask(self, mask: int, *, includeZero: bool = False)->Iterator[int]:
        """部分集合を返却します"""
        mask &= self.full
        sub = mask
        while sub:
            yield sub
            sub = (sub - 1) & mask
        if includeZero:
            yield 0
    
    def remainSubMask(self, mask: int, *, includeZero: bool = False)->Iterator[int]:
        """補集合の部分集合を返却します"""
        mask &= self.full
        remain = self.full ^  mask
        sub = remain
        while sub:
            yield sub
            sub = (sub - 1) & remain
        if includeZero:
            yield 0

    def subMaskTuple(self, mask: int, *, includeZero: bool = False)->Iterator[Tuple[int, ...]]:
        """部分集合をタプルで返却します"""
        mask &= self.full
        sub = mask
        while sub:
            yield self.toTuple(sub)
            sub = (sub - 1) & mask
        if includeZero:
            yield self.toTuple(0)

    def remainSubMaskTuple(self, mask: int, *, includeZero: bool = False)->Iterator[Tuple[int, ...]]:
        """補集合の部分集合をタプルで返却します"""
        mask &= self.full
        remain = self.full ^  mask
        sub = remain
        while sub:
            yield self.toTuple(sub)
            sub = (sub - 1) & remain
        if includeZero:
            yield self.toTuple(0)
    
    def popcount(self, mask: int)-> int:
        """1の個数を返却します"""
        return (mask&self.full).bit_count()
    
    def getPopIndex(self, mask: int)->Tuple[int, ...]:
        """bitが立っている位置を取得します"""
        result = []
        mask &= self.full
        b = 1
        for i in range(self.n):
            if mask & b:
                result.append(i)
            b <<= 1
        return tuple(result)

    def __len__(self)->int:
        return self.n


# AWC0003E
N, M = map(int, input().split())
W = list(map(int, input().split()))
C = list(map(int, input().split()))
C.sort(reverse=True)
Mx = 1 << N
bm = BitMapper(N)
remainSubMask = bm.remainSubMask
weight = [0] * Mx
for mask in range(1, Mx):
    lsb = mask & -mask
    i = (lsb.bit_length() - 1)
    weight[mask] = weight[mask^lsb] + W[i]

okMask = [0]
dp = [False] * Mx
dp[0] = True
for capa in C:
    newDP = dp[:]
    newOkMask = okMask[:]
    for mask in okMask:
        if not dp[mask]:
            continue
        for dat in remainSubMask(mask):
            if weight[dat] > capa:
                continue
            newMask = dat|mask
            if not newDP[newMask]:
                newDP[newMask] = True
                newOkMask.append(newMask)
    dp = newDP
    okMask = newOkMask
    if dp[Mx-1]:
        break
print("Yes" if dp[Mx-1] else "No")
