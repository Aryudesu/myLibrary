from sortedcontainers import SortedList

class BestKthSum:
    """
    上位K番目の値の総和を計算します．
    値の更新がされることを考慮．
    """
    def __init__(self, K: int, values: list[int] = [0]):
        self.k = K
        self.data = list(values)
        self.n = len(self.data)
        self.sorted = SortedList(-x for x in self.data)
        self.sum = 0
        for k in range(K):
            self.sum += self.sorted[k]
    
    def update(self, idx: int, new_val: int)-> int:
        K = self.k
        sortedData = self.sorted

        # 変数設定
        kth = -sortedData[K-1]
        prev = self.data[idx]
        now = new_val
        self.data[idx] = now
        # ソート結果の更新
        sortedData.discard(-prev)
        sortedData.add(-now)
        # 上位K番目の値を取得
        next_kth = -sortedData[K - 1]

        # 入る値
        self.sum += max(next_kth, now)

        # 外れる値
        if prev > next_kth:
            self.sum -= prev
        else:
            self.sum -= kth

        return self.sum


# === ABC306 E

N, K, Q = map(int, input().split())
bks = BestKthSum(K, [0] * N)
result = []
for q in range(Q):
    X, Y = map(int, input().split())
    result.append(bks.update(X-1, Y))
for r in result:
    print(r)
    
