class Queue:
    """キュー"""
    def __init__(self, A=[]) -> None:
        """初期化"""
        self.pointerL = 0
        self.pointerR = 0
        self.data = []
        for a in A:
            self.data.append(a)
            self.pointerR += 1

    def queue(self, a):
        """データの追加"""
        if self.pointerR < len(self.data):
            self.data[self.pointerR] = a
            self.pointerR += 1
        else:
            self.data.append(a)
            self.pointerR += 1

    def dequeueL(self):
        """左からデータの取り出し・削除"""
        res = self.data[self.pointerL]
        self.pointerL += 1
        return res

    def dequeueR(self):
        """右からデータの取り出し・削除"""
        res = self.data[self.pointerR - 1]
        self.pointerR -= 1
        return res

    def getL(self):
        """左のデータの取り出し"""
        return self.data[self.pointerL]

    def getR(self):
        """右のデータの取り出し"""
        return self.data[self.pointerR - 1]

# *** Example (プログラミングの鉄則 A52) ***
Q = int(input())
qu = Queue()
result = []
for q in range(Q):
    query = [l for l in input().split()]
    if query[0] == "1":
        qu.queue(query[1])
    elif query[0] == "2":
        result.append(qu.getL())
    elif query[0] == "3":
        qu.dequeueL()
for r in result:
    print(r)
