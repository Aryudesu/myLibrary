def circularWeightedDistance(W):
    """全終点 x の sum(W[i]*((x-i)%N)) を O(N) で返す。
    辺は i -> (i+1)%N。負の重み可。空列なら []。
    """
    W = list(W)
    n = len(W)
    if not n:
        return []
    total = sum(W)
    cur = sum((n-i)*W[i] for i in range(1,n))
    result = [cur]
    for i in range(1,n):
        cur += total - n*W[i]
        result.append(cur)
    return result


class CircularWeightedDistance:
    """円環上の有向重み付き距離和を前計算する。"""
    def __init__(self, W):
        self.result = circularWeightedDistance(W)

    def get(self, x):
        return self.result[x]

    def getAll(self):
        return self.result[:]
