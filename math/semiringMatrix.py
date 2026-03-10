class SemiringMatrix:
    """
    半環行列
    add: 加法演算
    mul: 乗法演算
    zero: 加法単位元
    one: 乗法単位元
    """

    __slots__ = ("a", "n", "m", "add", "mul", "zero", "one")

    def __init__(self, a, add, mul, zero, one):
        assert a and a[0]
        m = len(a[0])
        assert all(len(row) == m for row in a)

        self.a = [row[:] for row in a]
        self.n = len(a)
        self.m = m
        self.add = add
        self.mul = mul
        self.zero = zero
        self.one = one

    @classmethod
    def zeros(cls, n, m, add, mul, zero, one):
        return cls([[zero] * m for _ in range(n)], add, mul, zero, one)

    @classmethod
    def identity(cls, n, add, mul, zero, one):
        res = [[zero] * n for _ in range(n)]
        for i in range(n):
            res[i][i] = one
        return cls(res, add, mul, zero, one)

    def copy(self):
        return SemiringMatrix(self.a, self.add, self.mul, self.zero, self.one)

    def __getitem__(self, i):
        return self.a[i]

    def __repr__(self):
        return "\n".join(" ".join(map(str, row)) for row in self.a)

    @property
    def shape(self):
        return (self.n, self.m)

    def matmul(self, other):
        """行列積 self @ other"""
        assert self.m == other.n
        assert self.add is other.add
        assert self.mul is other.mul
        assert self.zero == other.zero
        assert self.one == other.one

        res = [[self.zero] * other.m for _ in range(self.n)]

        # 普通の三重ループ
        for i in range(self.n):
            ai = self.a[i]
            ri = res[i]
            for k in range(self.m):
                aik = ai[k]
                ok = other.a[k]
                for j in range(other.m):
                    ri[j] = self.add(ri[j], self.mul(aik, ok[j]))

        return SemiringMatrix(res, self.add, self.mul, self.zero, self.one)

    def __matmul__(self, other):
        return self.matmul(other)

    def transpose(self):
        return SemiringMatrix(
            [list(col) for col in zip(*self.a)],
            self.add, self.mul, self.zero, self.one
        )

    def pow(self, k):
        """self^k"""
        assert self.n == self.m
        assert k >= 0

        res = SemiringMatrix.identity(
            self.n, self.add, self.mul, self.zero, self.one
        )
        base = self.copy()

        while k:
            if k & 1:
                res = res.matmul(base)
            base = base.matmul(base)
            k >>= 1

        return res

    def matvec(self, vec):
        """
        行列 × 列ベクトル
        self(n*m) @ vec(m)
        戻り値は長さ n の list
        """
        assert len(vec) == self.m
        res = [self.zero] * self.n
        for i in range(self.n):
            s = self.zero
            row = self.a[i]
            for k in range(self.m):
                s = self.add(s, self.mul(row[k], vec[k]))
            res[i] = s
        return res

    def vecmat(self, vec):
        """
        行ベクトル × 行列
        vec(n) @ self(n*m)
        戻り値は長さ m の list
        """
        assert len(vec) == self.n
        res = [self.zero] * self.m
        for k in range(self.n):
            vk = vec[k]
            row = self.a[k]
            for j in range(self.m):
                res[j] = self.add(res[j], self.mul(vk, row[j]))
        return res

    def pow_apply_matvec(self, k, vec):
        """
        (self^k) @ vec
        列ベクトルに右から作用させる版
        """
        assert self.n == self.m
        assert len(vec) == self.m
        assert k >= 0

        base = self.copy()
        res_vec = vec[:]

        first = True
        while k:
            if k & 1:
                if first:
                    res_vec = base.matvec(res_vec)
                    first = False
                else:
                    res_vec = base.matvec(res_vec)
            base = base.matmul(base)
            k >>= 1

        return res_vec

    def pow_apply_vecmat(self, k, vec):
        """
        vec @ (self^k)
        行ベクトルに左から作用させる版
        """
        assert self.n == self.m
        assert len(vec) == self.n
        assert k >= 0

        base = self.copy()
        res_vec = vec[:]

        while k:
            if k & 1:
                res_vec = base.vecmat(res_vec)  # これは後で注意、下の修正版参照
            base = base.matmul(base)
            k >>= 1

        return res_vec


# === AWC0021 E
def mul(a: int, b: int)-> int:
    return a + b
INF = 10 ** 18
N, a, b = map(int, input().split())
M = SemiringMatrix([[a//2, a], [b//2, b]], max, mul, -INF, 0)
res = M.pow_apply_matvec(N, [-INF, 0])
print(max(res))
