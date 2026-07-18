from typing import Tuple
class LinearDiffMin:
    def __init__(self, INF: int = 10 ** 18):
        self.INF = INF
        self.lineData: list[Tuple[int, int]] = []

    def addLinear(self, a: int, b: int)->int:
        """直線ax + bを追加し，直線のIDを返却します"""
        self.lineData.append((a, b))
        return len(self.lineData) - 1

    def changeLine(self, lineId: int, a: int, b: int):
        """IDを指定し，その直線の定義を変更します"""
        assert 0 <= lineId < len(self.lineData)
        self.lineData[lineId] = (a, b)
    
    def calcDiff(self, x: int, *, ignore: set[int]|None = None, target: set[int]|None = None)->int:
        """xにおける最大値と最小値の差を取得します"""
        assert ignore is None or target is None
        M = -self.INF
        m = self.INF
        for lineId in range(len(self.lineData)):
            if ignore is not None and lineId in ignore:
                continue
            if target is not None and lineId not in target:
                continue
            a, b = self.lineData[lineId]
            M = max(M, a*x + b)
            m = min(m, a*x + b)
        return M - m

    def calcArgDiffMin(self, L: int, R: int, *, ignore: set[int]|None = None, target: set[int]|None = None)->int:
        """ L 以上 R 以下の範囲でlinearの最大値と最小値の差が最小となるxを計算します """
        assert ignore is None or target is None
        ng = L - 1
        ok = R
        while ok - ng > 1:
            mid = (ok + ng) // 2
            if self.calcDiff(mid+1, ignore, target) < self.calcDiff(mid, ignore, target):
                ng = mid
            else:
                ok = mid
        return ok

    def calcDiffMin(self, L: int, R: int, *, ignore: set[int]|None = None, target: set[int]|None = None)->int:
        x = self.calcArgDiffMin(L, R, ignore=ignore, target=target)
        return self.calcDiff(x, ignore=ignore, target=target)


# AWC0115 D
N, D, Q = map(int, input().split())
ldm = LinearDiffMin()
for _ in range(N):
    x, v, l = map(int, input().split())
    ldm.addLinear(v, x + l)
    ldm.addLinear(v, x - l)

result = []
result.append(ldm.calcDiff(ldm.calcArgDiffMin(0, D)))
for _ in range(Q):
    p, a, b, c = map(int, input().split())
    ldm.changeLine((p-1)*2, b, a+c)
    ldm.changeLine((p-1)*2+1, b, a-c)
    result.append(ldm.calcDcalcDiffMiniff(0, D))
print(*result, sep="\n")
