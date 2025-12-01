from atcoder.fenwicktree import FenwickTree

class CountRangeSum:
    """範囲についての値の個数と範囲についての総和を考える"""
    def __init__(self, maxValue: int = 200000):
        self.maxValue = maxValue
        self.n = maxValue + 2
        self.cnt = FenwickTree(self.n)
        self.val = FenwickTree(self.n)
        self.total = 0
    
    def getAllCnt(self):
        """全ての値の個数を返却します"""
        return self.total

    def addNum(self, value: int, num: int = 1):
        """値(value)を指定個(num個)追加"""
        self.cnt.add(value, num)
        self.val.add(value, value*num)
        self.total += num

    def rangeSum(self, l: int, r: int) -> int:
        """l以上r未満の値の総和"""
        return self.val.sum(l, r)
    
    def rangeCnt(self, l: int, r: int) -> int:
        """l以上r未満の値の個数"""
        return self.cnt.sum(l, r)
    
    def countLt(self, l: int) -> int:
        """l未満の値の個数"""
        return self.cnt.sum(0, l)
    
    def sumLt(self, l: int) -> int:
        """l未満の値の総和"""
        return self.val.sum(0, l)
    
    def countGeq(self, r: int) -> int:
        """r以上の値の個数"""
        return self.cnt.sum(r, self.n)

    def sumGeq(self, r: int) -> int:
        """r以上の値の総和"""
        return self.val.sum(r, self.n)
    
    def kth(self, k: int) -> int:
        assert 0 <= k < self.total
        data: list[int] = self.cnt.data
        idx = 0
        s = 0
        bit = 1 << (self.n.bit_length() - 1)
        while bit > 0:
            nxt = idx + bit
            if nxt <= self.n and s + data[nxt - 1] <= k:
                s += data[nxt - 1]
                idx = nxt
            bit >>= 1
        return idx

crs = CountRangeSum()
data = [1, 1, 100, 7, 5]
for n in data:
    crs.addNum(n)
for i in range(len(data)):
    print(crs.kth(i))


# === ABC432E
# N, Q = map(int, input().split())
# A = list(map(int, input().split()))
# crs = CountRangeSum(500000)
# for a in A:
#     crs.addNum(a)
# result = []
# for _ in range(Q):
#     n, *query = map(int, input().split())
#     if n == 1:
#         x, y = query
#         x -= 1
#         crs.addNum(A[x], -1)
#         crs.addNum(y)
#         A[x] = y
#     elif n == 2:
#         l, r = query
#         if l > r:
#             result.append(l * N)
#         else:
#             lSum = crs.countLt(l) * l
#             mSum = crs.rangeSum(l, r)
#             rSum = crs.countGeq(r) * r
#             result.append(lSum + mSum + rSum)
#     else:
#         raise Exception()
# for r in result:
#     print(r)
