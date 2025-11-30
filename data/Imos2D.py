class Imos2D:
    """0-indexed座標での2次元いもす法用ライブラリ"""
    def __init__(self, H: int, W: int)->None:
        self.data = [[0] * W for _ in range(H)]
        self.H = H
        self.W = W
        self._num = 0
        self.initialized = False

    def add(self, u: int, l: int, d: int, r: int, x: int = 1)->None:
        """(u, l)を左上，(d, r)を右下とする矩形にxを加算します"""
        assert not self.initialized
        u_ = max(0, u)
        l_ = max(0, l)
        d_ = min(d, self.H-1)
        r_ = min(r, self.W-1)
        if u_ > d_ or l_ > r_:
            return
        self.data[u_][l_] += x
        if r_ + 1 < self.W:
            self.data[u_][r_ + 1] -= x
        if d_ + 1 < self.H:
            self.data[d_+1][l_] -= x
        if d_ + 1 < self.H and r_ + 1 < self.W:
            self.data[d_+1][r_+1] += x
        self._num += 1

    def build(self)->None:
        """計算を行います"""
        assert not self.initialized
        for h in range(self.H):
            tmp = 0
            for w in range(self.W):
                tmp += self.data[h][w]
                self.data[h][w] = tmp
        for w in range(self.W):
            tmp = 0
            for h in range(self.H):
                tmp += self.data[h][w]
                self.data[h][w] = tmp
        self.initialized = True
    
    def get(self, h: int, w: int)->int:
        """
        (h, w)の座標の値を取得します．
        buildを行った後でないとExceptionがraiseされます
        """
        assert self.initialized
        assert 0 <= h < self.H
        assert 0 <= w < self.W
        return self.data[h][w]

    def getData(self)->list[list[int]]:
        """
        build後の生データ（内部参照）を取得します．
        buildを行った後でないとExceptionがraiseされます
        """
        assert self.initialized
        return self.data

    def cells(self):
        """
        グリッドに対してのループ処理を行います
        各マスに対して(h, w, value)をyieldします
        """
        assert self.initialized
        for h in range(self.H):
            row = self.data[h]
            for w in range(self.W):
                yield h, w, row[w]
    
    def rows(self):
        """H*Wの範囲についての各行のデータ（長さWのリスト）を順に返却します"""
        assert self.initialized
        for dat in self.data:
            yield dat

    @staticmethod
    def zipCells(a: "Imos2D", b: "Imos2D"):
        """
        2つのいもす法のグリッドに対してのループ処理を行います
        各マスに対して(h, w, value1, value2)をyieldします
        """
        assert a.initialized and b.initialized
        assert a.H == b.H and a.W == b.W
        H, W = a.H, a.W
        dataA = a.data
        dataB = b.data
        for h in range(H):
            rowA = dataA[h]
            rowB = dataB[h]
            for w in range(W):
                yield h, w, rowA[w], rowB[w]

    def __len__(self)->int:
        """グリッドに反映されたデータの個数を返却します"""
        return self._num


# ==== ABC434D
N = int(input())
H, W = 2000, 2000
sky1 = Imos2D(H, W)
sky2 = Imos2D(H, W)
for n in range(N):
    u, d, l, r = map(int, input().split())
    sky1.add(u-1, l-1, d-1, r-1)
    sky2.add(u-1, l-1, d-1, r-1, n + 1)

sky1.build()
sky2.build()
data = [0] * N
allCloud = 0
for h, w, v1, v2 in Imos2D.zipCells(sky1, sky2):
    if v1 > 0:
        allCloud += 1
    if v1 == 1:
        data[v2 - 1] += 1

for dat in data:
    print(H*W - allCloud + dat)
