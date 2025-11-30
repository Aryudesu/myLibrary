class PrefixSum3D:
    """0-indexed座標での3次元累積和用ライブラリ"""
    def __init__(self, X: int, Y: int, Z: int) -> None:
        self.X = X
        self.Y = Y
        self.Z = Z
        self.orig = [[[0] * Z for _ in range(Y)] for _ in range(X)]
        self.sums = [[[0] * (Z + 1) for _ in range(Y + 1)] for _ in range(X + 1)]
        self.initialized = False

    def add(self, x: int, y: int, z: int, v: int) -> None:
        """(x, y, z) に値 v を加算します"""
        assert not self.initialized
        if 0 <= x < self.X and 0 <= y < self.Y and 0 <= z < self.Z:
            self.orig[x][y][z] += v

    def set(self, x: int, y: int, z: int, v: int) -> None:
        """(x, y, z) の値を v に設定します"""
        assert not self.initialized
        if 0 <= x < self.X and 0 <= y < self.Y and 0 <= z < self.Z:
            self.orig[x][y][z] = v

    def build(self) -> None:
        """3次元累積和を計算します"""
        assert not self.initialized
        X, Y, Z = self.X, self.Y, self.Z
        ps = self.sums
        a = self.orig
        for x in range(X):
            for y in range(Y):
                for z in range(Z):
                    ps[x+1][y+1][z+1] = (
                        a[x][y][z]
                        + ps[x][y+1][z+1]
                        + ps[x+1][y][z+1]
                        + ps[x+1][y+1][z]
                        - ps[x][y][z+1]
                        - ps[x][y+1][z]
                        - ps[x+1][y][z]
                        + ps[x][y][z]
                    )
        self.initialized = True

    def sum(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> int:
        """
        (x1, y1, z1) を左上手前、(x2, y2, z2) を右下奥とする直方体領域（両端含む）の総和を返却します。
        """
        assert self.initialized
        assert 0 <= x1 <= x2 < self.X
        assert 0 <= y1 <= y2 < self.Y
        assert 0 <= z1 <= z2 < self.Z
        ps = self.sums

        X1, Y1, Z1 = x1, y1, z1
        X2, Y2, Z2 = x2 + 1, y2 + 1, z2 + 1

        return (
            ps[X2][Y2][Z2]
            - ps[X1][Y2][Z2]
            - ps[X2][Y1][Z2]
            - ps[X2][Y2][Z1]
            + ps[X1][Y1][Z2]
            + ps[X1][Y2][Z1]
            + ps[X2][Y1][Z1]
            - ps[X1][Y1][Z1]
        )

    def getData(self) -> list[list[list[int]]]:
        """元のX×Y×Zデータを返却します"""
        return self.orig

    @classmethod
    def makeData(cls, grid: list[list[list[int]]]) -> "PrefixSum3D":
        """既存の3次元グリッドから累積和を構築します"""
        X = len(grid)
        Y = len(grid[0]) if X > 0 else 0
        Z = len(grid[0][0]) if Y > 0 else 0
        obj = cls(X, Y, Z)
        for x in range(X):
            for y in range(Y):
                row_src = grid[x][y]
                row_dst = obj.orig[x][y]
                for z in range(Z):
                    row_dst[z] = row_src[z]
        obj.build()
        return obj

N = int(input())
A = []
for n in range(N):
    tmp = []
    for m in range(N):
        tmp.append(list(map(int, input().split())))
    A.append(tmp)
ps = PrefixSum3D.makeData(A)
result = []
Q = int(input())
for _ in range(Q):
    Lx1, Rx1, Ly1, Ry1, Lz1, Rz1 = map(int, input().split())
    result.append(ps.sum(Lx1-1, Ly1-1, Lz1-1, Rx1-1, Ry1-1, Rz1-1))
for r in result:
    print(r)
