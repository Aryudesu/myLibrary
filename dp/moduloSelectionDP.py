class ModuloSelectionDP:
    """各回の候補から1つ選んだ総和の剰余ごとの通り数。
    同値・同剰余の候補も区別する。負数可。mod=None なら厳密整数。
    step: O(m*L+m)（Lは候補数）、空間 O(m+L)。
    """
    def __init__(self, m, mod=998244353):
        if m <= 0 or (mod is not None and mod <= 0):
            raise ValueError("invalid modulus")
        self.m, self.mod = m, mod
        self.dp = [0]*m
        self.dp[0] = 1 if mod is None else 1 % mod

    def step(self, choices):
        m, mod, old = self.m, self.mod, self.dp
        choices = [a % m for a in choices]
        if len(choices) == 2:
            a, b = choices
            nxt = [old[(i-a)%m] + old[(i-b)%m] for i in range(m)]
        else:
            nxt = [0]*m
            for a in choices:
                for i in range(m):
                    nxt[i] += old[(i-a)%m]
        self.dp = nxt if mod is None else [x % mod for x in nxt]

    def get(self, x):
        return self.dp[x % self.m]
