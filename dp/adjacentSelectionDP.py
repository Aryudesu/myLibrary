class AdjacentSelectionDP:
    """各位置の候補から1つ選び、隣接条件の成立回数を数える。
    predicate(prev, cur) が真の回数を最大 k まで保持する。
    同値の候補も別の選択として数える。mod=None なら厳密整数。
    step: O((k+1)*前回候補数*今回候補数)、空間 O((k+1)*候補数)。
    """
    def __init__(self, k, predicate=lambda a, b: a == b, mod=998244353):
        if k < 0 or (mod is not None and mod <= 0):
            raise ValueError("invalid k or mod")
        self.k, self.predicate, self.mod = k, predicate, mod
        self.prev = None
        self.dp = []

    def step(self, choices):
        cur = list(choices)
        k, mod = self.k, self.mod
        nxt = [[0]*(k+1) for _ in cur]
        if self.prev is None:
            for row in nxt:
                row[0] = 1 if mod is None else 1 % mod
        else:
            for i, a in enumerate(self.prev):
                old = self.dp[i]
                for j, b in enumerate(cur):
                    d = int(bool(self.predicate(a, b)))
                    row = nxt[j]
                    for c in range(k+1-d):
                        value = row[c+d] + old[c]
                        row[c+d] = value if mod is None else value % mod
        self.prev, self.dp = cur, nxt

    def get(self, k):
        """成立回数がちょうど k の選び方。空列は0回の1通り。"""
        if not 0 <= k <= self.k:
            raise IndexError(k)
        ans = int(k == 0) if self.prev is None else sum(row[k] for row in self.dp)
        return ans if self.mod is None else ans % self.mod
