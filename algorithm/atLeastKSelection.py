from heapq import nsmallest


class AtLeastKSelection:
    """各組 (a,b) の一方を選び、Bの選択個数を制約する最小費用。
    費用は有限整数（負数可）。不可能なら float('inf')。
    add O(1)、初回問い合わせ O(N log N)、以降 O(1)。
    """
    def __init__(self, pairs=()):
        self.base = 0
        self.diffs = []
        self.prefix = None
        for a,b in pairs:
            self.add(a,b)

    def add(self, a, b):
        self.base += a
        self.diffs.append(b-a)
        self.prefix = None

    def _build(self):
        if self.prefix is not None:
            return
        ds = sorted(self.diffs)
        self.prefix = [self.base]
        self.neg = 0
        for d in ds:
            self.prefix.append(self.prefix[-1]+d)
            self.neg += d < 0

    def getMinCostExactly(self, k):
        if not 0 <= k <= len(self.diffs):
            return float("inf")
        self._build()
        return self.prefix[k]

    def getMinCostAtLeast(self, k):
        if not 0 <= k <= len(self.diffs):
            return float("inf")
        self._build()
        return self.prefix[max(k,self.neg)]

    def getMinCost(self, k):
        return self.getMinCostAtLeast(k)

    @staticmethod
    def solveAtLeast(pairs, k):
        """単発クエリ。負差分を先に採用し、不足分だけ heap で選ぶ。
        有限整数の費用を想定。O(N log(min(K,N)+2))、K固定なら O(N)。
        """
        if k < 0:
            return float("inf")
        total = count = 0
        positive = []
        for a,b in pairs:
            if b <= a:
                total += b
                count += 1
            else:
                total += a
                positive.append(b-a)
        need = max(0,k-count)
        if need > len(positive):
            return float("inf")
        return total + sum(nsmallest(need,positive))
