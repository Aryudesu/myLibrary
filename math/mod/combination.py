class Combination:
    def __init__(self, n, mod):
        self.mod = mod
        self.fact = [1] * (n + 1)
        self.inv_fact = [1] * (n + 1)
        for i in range(2, n + 1):
            self.fact[i] = self.fact[i - 1] * i % mod
        self.inv_fact[n] = pow(self.fact[n], mod - 2, mod)  # フェルマーの小定理
        for i in range(n - 1, 0, -1):
            self.inv_fact[i] = self.inv_fact[i + 1] * (i + 1) % mod

    def comb(self, n, k):
        if n < k or k < 0:
            return 0
        return (
            self.fact[n] * self.inv_fact[k] % self.mod * self.inv_fact[n - k] % self.mod
        )
