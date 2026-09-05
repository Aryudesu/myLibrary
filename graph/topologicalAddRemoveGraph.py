from collections import deque, defaultdict


class TopologicalGraph:
    """
    多重辺・辺追加削除対応の有向グラフ。

    頂点は 0-indexed。
    """

    def __init__(self, n: int):
        self.n = n
        self.graph = [set() for _ in range(n)]
        self.edge_count = defaultdict(int)
        self.indegree = [0] * n

    def add_edge(self, u: int, v: int) -> None:
        """辺の追加"""
        key = (u, v)

        if self.edge_count[key] == 0:
            self.graph[u].add(v)
            self.indegree[v] += 1

        self.edge_count[key] += 1

    def remove_edge(self, u: int, v: int) -> bool:
        """辺の削除"""
        key = (u, v)

        if self.edge_count[key] == 0:
            return False

        self.edge_count[key] -= 1

        if self.edge_count[key] == 0:
            self.graph[u].remove(v)
            self.indegree[v] -= 1

        return True

    def add_path(self, path: list[int]) -> None:
        """パス追加"""
        for u, v in zip(path, path[1:]):
            self.add_edge(u, v)

    def remove_path(self, path: list[int]) -> None:
        """パス削除"""
        for u, v in zip(path, path[1:]):
            self.remove_edge(u, v)

    def has_edge(self, u: int, v: int) -> bool:
        """辺があるか"""
        return self.edge_count[(u, v)] > 0

    def edge_multiplicity(self, u: int, v: int) -> int:
        """多重辺の本数"""
        return self.edge_count[(u, v)]

    def topological_sort(self) -> list[int]:
        """トポソ実行"""
        indegree = self.indegree.copy()
        queue = deque(
            v for v in range(self.n)
            if indegree[v] == 0
        )

        order = []

        while queue:
            v = queue.popleft()
            order.append(v)

            for nv in self.graph[v]:
                indegree[nv] -= 1

                if indegree[nv] == 0:
                    queue.append(nv)

        if len(order) != self.n:
            return []

        return order

    def is_dag(self) -> bool:
        """有向サイクルが存在しないグラフか"""
        return len(self.topological_sort()) == self.n