from atcoder.fenwicktree import FenwickTree
from sortedcontainers import SortedList

class kthSumFenwickTree:
    """サイズNの配列について上位K個の総和を計算するライブラリ"""
    def __init__(self, N: int, initVals: list[int]|None = None):
        self.n = N
        # 値保存用
        self.vals = [0] * N
        # 計算用
        self.sum = None
        self.num = None
        self.sorted = SortedList()
        # 座標圧縮用
        self.id = None
        self.inv = None
        # 初期化確認用
        self.initialized = False
        # 初期化
        if not initVals is None:
            self.setNumList(initVals)
    
    # 座標圧縮
    def setNumList(self, vals: list[int]):
        """使用する数値データについて座標圧縮を行います"""
        set_vals = set(vals)
        set_vals.add(0)
        self.inv = sorted(set_vals)
        self.id = {x: i for i, x in enumerate(self.inv)}

        self.sum = FenwickTree(len(self.inv))
        self.num = FenwickTree(len(self.inv))
        self.initialized = True

        for v in self.vals:
            self.sorted.add(v)
            idx = self.id[v]
            self.sum.add(idx, v)
            self.num.add(idx, 1)
    
    def _getId(self, data)-> int:
        assert self.initialized
        return self.id[data]
    
    def _getVal(self, id: int):
        assert self.initialized
        return self.inv[id]

    def initArray(self, data: list[int]):
        for i in range(min(self.n, len(data))):
            self.change(i, data[i])

    # 以下計算部
    def change(self, p, x):
        """pにxを代入"""
        assert self.initialized
        prev = self.vals[p]
        if prev == x:
            return
        self.vals[p] = x
        # データ更新
        self.sorted.discard(prev)
        self.sorted.add(x)
        prevId = self._getId(prev)
        nextId = self._getId(x)
        self.sum.add(prevId, -prev)
        self.sum.add(nextId, x)
        self.num.add(prevId, -1)
        self.num.add(nextId, 1)

    def add(self, p, x):
        """pにxを加算"""
        assert self.initialized
        prev = self.vals[p]
        self.change(p, prev + x)

    def getKthSmallestSum(self, k: int):
        """下位k番目の値の総和を取得"""
        assert self.initialized
        kthVal = self.sorted[k-1]
        id = self._getId(kthVal)
        r = self.num.sum(0, id + 1)
        s = self.sum.sum(0, id + 1)
        return s - (r - k) * kthVal
    
    def getKthSum(self, k: int):
        """上位k番目の値の総和を取得"""
        assert self.initialized
        allCnt = self.num.sum(0, len(self.inv))
        allSum = self.sum.sum(0, len(self.inv))
        return allSum - self.getKthSmallestSum(allCnt - k)



data = [3, 1, 4, 1, 5]
update = [(2, 9, 3), (3, 2, 2), (0, 6, 4), (2, 5, 1)]
nums = data[:]
for p, x, k in update:
    nums.append(x)
nums.append(0)
ksft = kthSumFenwickTree(len(data), nums)

debug = [0, 0, 0, 0, 0]
for i in range(len(data)):
    debug[i] = data[i]
    ksft.change(i, data[i])
    tmp = ksft.getKthSum(k)
    print(debug, k, tmp)

for p, x, k in update:
    debug[p] = x
    ksft.change(p, x)
    tmp = ksft.getKthSum(k)
    print(debug, k, tmp)
