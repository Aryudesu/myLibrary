class Imos1D:
    """0-indexed座標での1次元いもす法用ライブラリ"""
    def __init__(self, N: int) -> None:
        self.data = [0] * N
        self.N = N
        self._num = 0
        self.initialized = False

    def add(self, l: int, r: int, x: int = 1) -> None:
        """[l, r] に x を加算します"""
        assert not self.initialized
        l_ = max(0, l)
        r_ = min(r, self.N - 1)
        if l_ > r_:
            return
        self.data[l_] += x
        if r_ + 1 < self.N:
            self.data[r_ + 1] -= x
        self._num += 1

    def build(self) -> None:
        """計算を行います"""
        assert not self.initialized
        s = 0
        for i in range(self.N):
            s += self.data[i]
            self.data[i] = s
        self.initialized = True

    def get(self, i: int) -> int:
        """
        i の座標の値を取得します．
        build を行った後でないと Exception が raise されます
        """
        assert self.initialized
        assert 0 <= i < self.N
        return self.data[i]

    def getData(self) -> list[int]:
        """
        build 後の生データ（内部参照）を取得します．
        build を行った後でないと Exception が raise されます
        """
        assert self.initialized
        return self.data

    def cells(self):
        """
        配列に対してのループ処理を行います
        各要素に対して(i, value)をyieldします
        """
        assert self.initialized
        for i, v in enumerate(self.data):
            yield i, v

    @staticmethod
    def zipCells(a: "Imos1D", b: "Imos1D"):
        """
        2つのいもす法配列に対してのループ処理を行います
        各要素に対して(i, value1, value2)をyieldします
        """
        assert a.initialized and b.initialized
        assert a.N == b.N
        for i in range(a.N):
            yield i, a.data[i], b.data[i]

    def __len__(self) -> int:
        """配列に反映されたデータの個数を返却します"""
        return self._num
    
    def __getitem__(self, i: int) -> int:
        assert self.initialized
        assert 0 <= i < self.N
        return self.data[i]

    def __iter__(self):
        assert self.initialized
        return iter(self.data)


#=== Sample AWC0048 C
N, M = map(int, input().split())
imos = Imos1D(N)
H = list(map(int, input().split()))
for m in range(M):
    l, r, d = map(int, input().split())
    imos.add(l-1, r-1, d)
imos.build()
result = 0
for i in range(N):
    if H[i] - imos[i] >= 1:
        result += 1
print(result)
