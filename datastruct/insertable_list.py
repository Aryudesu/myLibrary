class InsertableList:
    """
    挿入可能な配列管理用クラス
    同じ要素が2度使われないことが保証されていること前提
    """

    def __init__(self, Data):
        """初期設定"""
        self.arrayData = dict()
        N = len(Data)
        assert N > 0
        self.stNum = Data[0]
        check = set(Data)
        assert len(check) == len(Data)
        for i in range(N):
            prev = None
            aft = None
            if i > 0:
                prev = Data[i-1]
            if i < N - 1:
                aft = Data[i + 1]
            self.arrayData[Data[i]] = (prev, aft)

    def insert(self, x, y):
        """xの後にyを挿入します"""
        assert x in self.arrayData
        assert self.arrayData.get(y) is None
        tmp = self.arrayData[x]
        aftNum = tmp[1]
        if not aftNum is None:
            adata = self.arrayData[aftNum]
            self.arrayData[aftNum] = (y, adata[1])
        self.arrayData[y] = (x, aftNum)
        self.arrayData[x] = (tmp[0], y)

    def delete(self, x):
        """要素を削除します"""
        assert x in self.arrayData
        tmp = self.arrayData[x]
        prev, aft = tmp
        if not prev is None:
            ptmp = self.arrayData[prev]
            self.arrayData[prev] = (ptmp[0], aft)
        else:
            self.stNum = aft
        if not aft is None:
            atmp = self.arrayData[aft]
            self.arrayData[aft] = (prev, atmp[1])
        self.arrayData[x] = None

    def getArray(self):
        """配列でデータを取得します"""
        result = []
        num = self.stNum
        while not num is None:
            result.append(num)
            tmp = self.arrayData[num]
            num = tmp[1]
        return result

# *** Example (ABC344 E) ***
N = int(input())
A = [int(l) for l in input().split()]
IL = InsertableList(A)
Q = int(input())
for _ in range(Q):
    n, *q = [int(l) for l in input().split()]
    if n == 1:
        x, y = q
        IL.insert(x, y)
    else:
        x = q[0]
        IL.delete(x)
result = IL.getArray()
print(*result)
