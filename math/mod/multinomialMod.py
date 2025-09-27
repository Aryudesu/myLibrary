class MultinomialMod:
    """重複組合せ計算ライブラリ"""
    def __init__(self, MOD: int, N: int):
        """M: mod, maxN: 要素最大数"""
        self.MOD = MOD
        self.N = N
        self.factors = self._factorize(MOD)
        self.tables = {}
        for p, e in self.factors:
            self.tables[(p, e)] = self._buildTable(p, e, N)

    def _factorize(self, n: int) -> list[tuple[int, int]]:
        """素因数分解を行う． p^n = (p, n)で表現．"""
        fs = []
        d = 2
        while d * d <= n:
            if n % d == 0:
                e = 0
                while n % d == 0:
                    n //= d
                    e += 1
                fs.append((d, e))
            d = 3 if d == 2 else d + 2
        if n > 1:
            fs.append((n, 1))
        return fs

    def _egcd(self, a: int, b: int):
        """拡張ユークリッド互除法"""
        if b == 0:
            return (1, 0, a)
        x, y, g = self._egcd(b, a % b)
        return (y, x - (a // b) * y, g)

    def _invMod(self, a: int, m: int) -> int:
        """逆元計算を行う"""
        x, y, g = self._egcd(a, m)
        if g != 1:
            raise ZeroDivisionError
        return x % m

    def _buildTable(self, p: int, e: int, N: int):
        """事前計算"""
        mod = p ** e
        vp = [0] * (N + 1)
        gp = [1] * (N + 1)
        cnt = 0
        acc = 1
        for n in range(1, N + 1):
            x = n
            while x % p == 0:
                x //= p
                cnt += 1
            acc = (acc * (x % mod)) % mod
            vp[n] = cnt
            gp[n] = acc
        return (mod, vp, gp)

    def _calcOne(self, C: list[int], S: int, p: int, e: int, table) -> int:
        """素数冪での多項係数計算"""
        mod, vp, gp = table
        t = vp[S]
        den = 1
        for c in C:
            t -= vp[c]
            den = (den * gp[c]) % mod
        if t >= e:
            return 0
        num = gp[S]
        inv = self._invMod(den, mod)
        res = (num * inv) % mod
        res = (res * pow(p, t, mod)) % mod
        return res

    def _crt(self, a1: int, m1: int, a2: int, m2: int) -> tuple[int, int]:
        """中国の定理． x\equiv a1 (mod m1), x\equiv a2 (mod m2)の計算"""
        k = (a2 - a1) % m2
        inv = self._invMod(m1 % m2, m2)
        t = (k * inv) % m2
        return (a1 + m1 * t) % (m1 * m2), m1 * m2

    def calcMultinomial(self, C: list[int]) -> int:
        """重複組合せ計算"""
        S = sum(C)
        if S > self.N:
            raise ValueError("precompute maxN is too small")
        res, modNow = 0, 1
        for (p, e), table in self.tables.items():
            ai = self._calcOne(C, S, p, e, table)
            if modNow == 1:
                res, modNow = ai, p ** e
            else:
                res, modNow = self._crt(res, modNow, ai, p ** e)
        return res % self.MOD
