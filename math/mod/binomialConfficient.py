class BinomialCoefficient:
    def __init__(self, n: int, mod: int=998244353):
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
        if k < 0:
            return 0
        if n >= 0:
            if n < k:
                return 0
            return (((self.data[n] * self.inv_data[n-k]) % self.mod) * self.inv_data[k]) % self.mod
        if n < 0:
            return self.calc(k-n-1, k) if k % 2 == 0 else -self.calc(k-n-1, k)

bc = BinomialCoefficient(100)
for i in range(101):
    for j in range(i + 1):
        print(bc.calc(i, j), end=" ")
    print()
