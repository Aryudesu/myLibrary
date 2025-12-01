from heapq import heappop, heappush

class GlobalAddMinHeap:
    """全体に加算する処理を考慮した最小値に対するHeap処理"""
    def __init__(self):
        self.data = []
        self.commonNum = 0

    def addVal(self, x=0):
        """値を追加する"""
        heappush(self.data, x-self.commonNum)
    
    def addAll(self, x):
        """要素全体にxを加算する"""
        self.commonNum += x
    
    def minVal(self):
        """最小値を取得します"""
        return self.data[0] + self.commonNum

    def pop(self):
        """最小値を配列から1つ除外し，値を返却します"""
        return heappop(self.data) + self.commonNum

    def __len__(self):
        return len(self.data)


# === ABC212
qm = GlobalAddMinHeap()
result = []
Q = int(input())
for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 1:
        n, x = query
        qm.addVal(x)
    elif query[0] == 2:
        n, x = query
        qm.addAll(x)
    elif query[0] == 3:
        n = query[0]
        result.append(qm.pop())
    else:
        raise Exception("想定外のクエリ")
for r in result:
    print(r)
