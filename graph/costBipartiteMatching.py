"""コスト付き二部マッチング（ハンガリアン法）。

左側 N 頂点すべてを、右側 M 頂点の異なる頂点に割り当てる。
存在しない辺は使えない。負の整数コストにも対応。
最小化・最大化はそれぞれ独立に何度でも実行可能。

計算量: O(N^2 M) (N <= M)、空間 O(NM)。
"""

class CostBipartiteMatching:
    """0-indexed の左 N 頂点、右 M 頂点のコスト付き割り当て。"""

    def __init__(self, N: int, M: int):
        if N < 0 or M < 0:
            raise ValueError("N and M must be nonnegative")
        self.N = N
        self.M = M
        self._edges: list[dict[int, int]] = [{} for _ in range(N)]

    def addEdge(self, src: int, dst: int, cost: int) -> None:
        """辺 (src, dst) を追加する。同じ辺への再追加はコストを上書き。"""
        if not (0 <= src < self.N and 0 <= dst < self.M):
            raise IndexError("vertex out of range")
        self._edges[src][dst] = cost

    def _solve(self, maximize: bool) -> tuple[int, list[tuple[int, int]]] | None:
        n, m = self.N, self.M
        if n == 0:
            return 0, []
        if n > m or any(not row for row in self._edges):
            return None

        sign = -1 if maximize else 1
        max_abs = max(abs(c) for row in self._edges for c in row.values())
        # ダミーコストは、実在辺だけの完全割り当てより必ず不利にする
        inf = 2 * n * max_abs + 1
        a = [[inf] * (m + 1) for _ in range(n + 1)]
        for i, row in enumerate(self._edges, 1):
            for j, cost in row.items():
                a[i][j + 1] = sign * cost

        u = [0] * (n + 1)
        v = [0] * (m + 1)
        p = [0] * (m + 1)
        way = [0] * (m + 1)

        for i in range(1, n + 1):
            p[0] = i
            j0 = 0
            minv = [float("inf")] * (m + 1)
            used = [False] * (m + 1)
            while True:
                used[j0] = True
                i0 = p[j0]
                delta = float("inf")
                j1 = -1
                for j in range(1, m + 1):
                    if used[j]:
                        continue
                    cur = a[i0][j] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
                if delta == float("inf"):
                    return None
                for j in range(m + 1):
                    if used[j]:
                        u[p[j]] += delta
                        v[j] -= delta
                    else:
                        minv[j] -= delta
                j0 = j1
                if p[j0] == 0:
                    break
            while True:
                j1 = way[j0]
                p[j0] = p[j1]
                j0 = j1
                if j0 == 0:
                    break

        pairs = [(-1, -1)] * n
        for j in range(1, m + 1):
            if p[j]:
                pairs[p[j] - 1] = (p[j] - 1, j - 1)

        if any(j not in self._edges[i] for i, j in pairs):
            return None
        return sum(self._edges[i][j] for i, j in pairs), pairs

    def minCost(self) -> tuple[int, list[tuple[int, int]]] | None:
        """最小コストと頂点ペアのリストを返す。不可能なら None。"""
        return self._solve(False)

    def maxCost(self) -> tuple[int, list[tuple[int, int]]] | None:
        """最大コストと頂点ペアのリストを返す。不可能なら None。"""
        return self._solve(True)
