class Matrix:
    """競プロ向けの行列クラス"""

    __slots__ = ("data", "H", "W")

    def __init__(self, data: list[list[int]]):
        assert data and data[0]
        w = len(data[0])
        assert all(len(row) == w for row in data)
        self.data = [row[:] for row in data]
        self.H = len(data)
        self.W = w

    @staticmethod
    def zeros(h: int, w: int) -> "Matrix":
        return Matrix([[0] * w for _ in range(h)])

    @staticmethod
    def identity(n: int) -> "Matrix":
        res = [[0] * n for _ in range(n)]
        for i in range(n):
            res[i][i] = 1
        return Matrix(res)

    def copy(self) -> "Matrix":
        return Matrix(self.data)

    def __getitem__(self, i: int) -> list[int]:
        return self.data[i]

    def __repr__(self) -> str:
        return "\n".join(map(str, self.data))

    def transpose(self) -> "Matrix":
        return Matrix([list(col) for col in zip(*self.data)])

    def __add__(self, other: "Matrix") -> "Matrix":
        assert self.H == other.H and self.W == other.W
        return Matrix([
            [self.data[i][j] + other.data[i][j] for j in range(self.W)]
            for i in range(self.H)
        ])

    def __sub__(self, other: "Matrix") -> "Matrix":
        assert self.H == other.H and self.W == other.W
        return Matrix([
            [self.data[i][j] - other.data[i][j] for j in range(self.W)]
            for i in range(self.H)
        ])

    def hadamard(self, other: "Matrix") -> "Matrix":
        assert self.H == other.H and self.W == other.W
        return Matrix([
            [self.data[i][j] * other.data[i][j] for j in range(self.W)]
            for i in range(self.H)
        ])

    def __matmul__(self, other: "Matrix") -> "Matrix":
        """通常の行列積: A @ B"""
        assert self.W == other.H
        res = [[0] * other.W for _ in range(self.H)]
        other_t = list(zip(*other.data))  # 列アクセス高速化
        for i in range(self.H):
            row = self.data[i]
            for j in range(other.W):
                col = other_t[j]
                s = 0
                for k in range(self.W):
                    s += row[k] * col[k]
                res[i][j] = s
        return Matrix(res)

    def matmulMod(self, other: "Matrix", mod: int) -> "Matrix":
        assert self.W == other.H
        res = [[0] * other.W for _ in range(self.H)]
        other_t = list(zip(*other.data))
        for i in range(self.H):
            row = self.data[i]
            for j in range(other.W):
                col = other_t[j]
                s = 0
                for k in range(self.W):
                    s += row[k] * col[k]
                res[i][j] = s % mod
        return Matrix(res)

    def __pow__(self, n: int) -> "Matrix":
        assert self.H == self.W
        assert n >= 0
        res = Matrix.identity(self.H)
        base = self.copy()
        while n:
            if n & 1:
                res = res @ base
            base = base @ base
            n >>= 1
        return res

    def modPow(self, n: int, mod: int) -> "Matrix":
        assert self.H == self.W
        assert n >= 0
        res = Matrix.identity(self.H)
        base = Matrix([[x % mod for x in row] for row in self.data])
        while n:
            if n & 1:
                res = res.matmulMod(base, mod)
            base = base.matmulMod(base, mod)
            n >>= 1
        return res

    def det(self) -> int:
        """実数/整数想定の簡易版。O(N^3)"""
        assert self.H == self.W
        a = [row[:] for row in self.data]
        n = self.H
        det = 1
        for i in range(n):
            pivot = i
            while pivot < n and a[pivot][i] == 0:
                pivot += 1
            if pivot == n:
                return 0
            if pivot != i:
                a[i], a[pivot] = a[pivot], a[i]
                det *= -1
            det *= a[i][i]
            pivot_val = a[i][i]
            for j in range(i + 1, n):
                if a[j][i] == 0:
                    continue
                factor = a[j][i] / pivot_val
                for k in range(i, n):
                    a[j][k] -= a[i][k] * factor
        return det

# ABC357D
S = input()
L = len(S)
N = int(S)
MOD = 998244353
data = [[10**L, N], [0, 1]]
lg = Matrix(data)
lg2 = lg.modPow(N, MOD)
print(lg2.data[0][1])
