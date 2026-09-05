class Tree:
    """
    重み付き無向木の基本クラス。

    頂点は 0-indexed。
    辺の重みを省略した場合は 1 として扱う。

    Euler Tour や LCA を必要としない、木そのものの基本機能を提供する。
    """

    def __init__(self, n: int):
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.node_cost = [0] * n

    def add_edge(self, u: int, v: int, weight: int = 1) -> None:
        """無向辺 u-v を追加する。weight のデフォルトは 1。"""
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))

    def set_node_cost(self, costs: list[int]) -> None:
        """各頂点のコストを設定する。"""
        assert len(costs) == self.n
        self.node_cost = list(costs)

    def distances_from(self, start: int) -> list[int]:
        """start から各頂点への重み付き距離を返す。"""
        dist = [0] * self.n
        parent = [-2] * self.n
        parent[start] = -1
        stack = [start]

        while stack:
            v = stack.pop()
            for to, weight in self.graph[v]:
                if to == parent[v]:
                    continue
                parent[to] = v
                dist[to] = dist[v] + weight
                stack.append(to)

        return dist

    def longest_node(self, start: int) -> tuple[int, int]:
        """
        start から最も重み付き距離が遠い頂点とその距離を返す。

        辺重みが非負であることを想定する。
        """
        dist = self.distances_from(start)
        farthest = max(range(self.n), key=dist.__getitem__)
        return farthest, dist[farthest]

    def diameter(self) -> tuple[int, int, int]:
        """
        木の重み付き直径を (端点u, 端点v, 距離) で返す。

        辺重みが非負であることを想定する。
        """
        if self.n == 0:
            return -1, -1, 0
        u, _ = self.longest_node(0)
        v, dist = self.longest_node(u)
        return u, v, dist
