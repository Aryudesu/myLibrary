from heapq import heappop, heappush

class GlobalAddMaxHeap:
    """全体に加算する処理を考慮した最大値に対するHeap処理"""
    def __init__(self):
        self.data = []
        self.commonNum = 0

    def addVal(self, x: int=0):
        """値を追加します"""
        heappush(self.data, self.commonNum - x)
    
    def addAll(self, x: int):
        """全体にxを加算します"""
        self.commonNum += x
    
    def maxVal(self):
        """最大値を取得します"""
        return self.commonNum - self.data[0]

    def pop(self):
        """最大値を配列から1つ除外し，値を返却します"""
        return self.commonNum - heappop(self.data)

    def __len__(self):
        return len(self.data)


# === ABC379D
Q = int(input())
hg = GlobalAddMaxHeap()
result = []
for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 1:
        hg.addVal()
    elif query[0] == 2:
        T = query[1]
        hg.addAll(T)
    elif query[0] == 3:
        H = query[1]
        res = 0
        while len(hg) > 0:
            r = hg.pop()
            if r < H:
                hg.addVal(r)
                break
            res += 1
        result.append(res)
    else:
        raise Exception()

for r in result:
    print(r)

