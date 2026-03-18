from collections import deque
from heapq import heappush, heappop


class TopologicalSort:
    """トポロジカルソート用クラス（0-indexed）"""

    def __init__(self, n: int):
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.indegree = [0] * n

    def add_edge(self, u: int, v: int) -> None:
        """u -> v の辺を追加します"""
        self.graph[u].append(v)
        self.indegree[v] += 1

    def sort(self) -> list[int]:
        """通常のトポロジカルソートを返します．閉路がある場合は空配列を返します．"""
        indeg = self.indegree[:]
        q = deque(i for i in range(self.n) if indeg[i] == 0)
        order = []

        while q:
            v = q.popleft()
            order.append(v)
            for nv in self.graph[v]:
                indeg[nv] -= 1
                if indeg[nv] == 0:
                    q.append(nv)

        if len(order) != self.n:
            return []
        return order

    def sort_lexicographical(self) -> list[int]:
        """辞書順最小のトポロジカルソートを返します．閉路がある場合は空配列を返します．"""
        indeg = self.indegree[:]
        hq = []
        for i in range(self.n):
            if indeg[i] == 0:
                heappush(hq, i)

        order = []
        while hq:
            v = heappop(hq)
            order.append(v)
            for nv in self.graph[v]:
                indeg[nv] -= 1
                if indeg[nv] == 0:
                    heappush(hq, nv)

        if len(order) != self.n:
            return []
        return order

    def sort_unique(self) -> tuple[bool, list[int]]:
        """
        一意性判定付きトポロジカルソート
        戻り値: (一意であるか, 順序)
        """
        indeg = self.indegree[:]
        q = deque(i for i in range(self.n) if indeg[i] == 0)
        order = []
        is_unique = True

        while q:
            if len(q) > 1:
                is_unique = False
            v = q.popleft()
            order.append(v)
            for nv in self.graph[v]:
                indeg[nv] -= 1
                if indeg[nv] == 0:
                    q.append(nv)

        if len(order) != self.n:
            return False, []
        return is_unique, order

    def order_to_rank(self, order: list[int]) -> list[int]:
        """order[何番目] = 頂点番号 から rank[頂点番号] = 何番目(1-indexed) を作ります．"""
        if not order:
            return []
        rank = [0] * self.n
        for i, v in enumerate(order):
            rank[v] = i + 1
        return rank
