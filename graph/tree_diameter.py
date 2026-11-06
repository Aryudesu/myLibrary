from graph.tree import Tree


class TreeDiameter(Tree):
    """
    木の直径・中心・離心率を求めるクラス（0-indexed）。

    Tree を継承し、add_edge(u, v, weight=1) で構築する。
    辺重みは非負を想定し、中心は「頂点の中で離心率が最小のもの」とする。
    重み付き木では中心が3頂点以上になることもある。

    build() 後に使用できる属性:
        diameter_length      : 木の重み付き直径
        endpoints            : 直径の端点2個 (u, v)
        path                 : u から v までの直径パス（頂点列）
        centers              : 離心率が最小となる頂点のリスト
        radius               : 頂点中心に関する半径（最小離心率）
        eccentricities       : 各頂点の離心率
        peripheral_vertices  : いずれかの直径の端点になる全頂点
        dist_from_u          : 直径端点 u から各頂点への距離
        dist_from_v          : 直径端点 v から各頂点への距離

    各頂点 v の離心率は max(dist(u,v), dist(v,v_endpoint)) で計算できる。
    初期化 + build は O(N) 時間・空間（木の辺数 N-1）。
    add_edge() 後は build() が必要。
    """

    def __init__(self, n: int):
        super().__init__(n)
        self._diameter_built = False

    def add_edge(self, u: int, v: int, weight: int = 1) -> None:
        if weight < 0:
            raise ValueError("TreeDiameter requires non-negative edge weights")
        super().add_edge(u, v, weight)
        self._diameter_built = False

    def build(self) -> None:
        """直径・直径パス・中心などを一括計算する。"""
        n = self.n
        if n == 0:
            self.diameter_length = 0
            self.endpoints = (-1, -1)
            self.path = []
            self.centers = []
            self.radius = 0
            self.eccentricities = []
            self.peripheral_vertices = []
            self.dist_from_u = []
            self.dist_from_v = []
            self._diameter_built = True
            return

        u, v, diameter = super().diameter()
        self.diameter_length = diameter
        self.endpoints = (u, v)
        self.dist_from_u = self.distances_from(u)
        self.dist_from_v = self.distances_from(v)

        ecc = [
            max(self.dist_from_u[i], self.dist_from_v[i])
            for i in range(n)
        ]
        self.eccentricities = ecc
        self.radius = min(ecc)
        self.centers = [i for i in range(n) if ecc[i] == self.radius]
        self.peripheral_vertices = [i for i in range(n) if ecc[i] == diameter]

        # 始点 u を根にして親を復元する。再帰は使わない。
        parent = [-2] * n
        parent[u] = -1
        stack = [u]
        while stack:
            node = stack.pop()
            for to, _ in self.graph[node]:
                if to == parent[node]:
                    continue
                parent[to] = node
                stack.append(to)

        path = []
        node = v
        while node != -1:
            path.append(node)
            node = parent[node]
        self.path = path[::-1]
        self._diameter_built = True

    def _ensure_built(self) -> None:
        if not self._diameter_built:
            self.build()

    def get_eccentricity(self, v: int) -> int:
        """頂点 v から最も遠い頂点までの距離を返す。"""
        self._ensure_built()
        return self.eccentricities[v]

    def is_peripheral(self, v: int) -> bool:
        """頂点 v がある直径の端点になれるかを返す。"""
        self._ensure_built()
        return self.eccentricities[v] == self.diameter_length
