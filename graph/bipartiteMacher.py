from atcoder.maxflow import MFGraph

class FlowBipartiteMatching:
    """左側 N点, 右側 M点 の0-indexed二部グラフの最大マッチング用クラス"""
    def __init__(self, N: int, M: int):
        self.N = N
        self.M = M
        self.MBase = N
        self.mf = MFGraph(N + M + 2)
        self.s = N + M
        self.t = N + M + 1
        for n in range(N):
            self.mf.add_edge(self.s, n, 1)
        for m in range(M):
            self.mf.add_edge(self.MBase + m, self.t, 1)

    def addEdge(self, src: int, dst: int)->None:
        """左側の点から右側の点に辺を張ります"""
        assert 0 <= src < self.N
        assert 0 <= dst < self.M
        self.mf.add_edge(src, self.MBase + dst, 1)
    
    def maxMatching(self)->int:
        """最大マッチングの結果を計算します"""
        return self.mf.flow(self.s, self.t)

# === AWC0013E

N, M = map(int, input().split())
fm = FlowBipartiteMatching(N, M )
for n in range(N):
    K, *C = list(map(int, input().split()))
    for c in C:
        fm.addEdge(n, c-1)
print(fm.maxMatching())
