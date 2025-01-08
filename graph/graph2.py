class Graph:
    def __init__(self, A):
        """グラフ配列A[]を設定"""
        self.data = A
        self.N = len(A)

    def moveK(self, s, K):
        """sから初めてk回遷移した場合の到着点"""
        p = s
        count = 0
        cData = dict()
        while True:
            count += 1
            p = self.data[p]
            if count == K:
                return p + 1
            if p in cData:
                if (K - count) % (count - cData[p]) == 0:
                    return p + 1
            cData[p] = count

