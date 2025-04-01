class BinomialCoefficient:
    """二項係数を高速で計算します"""

    def __init__(self, n: int, mod: int = 998244353):
        self.mod = mod
        self.n = n
        self.inv_data = []
        self.data = []
        self.init_data()

    def init_data(self):
        tmp = 1
        for i in range(1, self.n + 1):
            self.data.append(tmp)
            tmp = (tmp * i) % self.mod
        self.data.append(tmp)
        tmp = pow(tmp, self.mod - 2, self.mod)
        for i in range(self.n):
            self.inv_data.append(tmp)
            tmp = (tmp * (self.n - i)) % self.mod
        self.inv_data.append(tmp)
        self.inv_data.reverse()

    def calc(self, n, k):
        """二項係数を計算しますnCk"""
        if n < k:
            return 0
        return (
            ((self.data[n] * self.inv_data[n - k]) % self.mod) * self.inv_data[k]
        ) % self.mod
