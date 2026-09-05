from collections import defaultdict, deque
from heapq import heappop, heappush


class TopologicalSort:
    """
    トポロジカルソート用有向グラフ（0-indexed）。

    - 通常のトポロジカルソート
    - 辞書順最小のトポロジカルソート
    - 順序の一意性判定
    - DAG判定
    - 多重辺対応
    - 辺・パスの追加削除

    同じ u -> v が複数本存在する場合、トポロジカルソート上は1本の制約として扱い、
    最後の1本を削除したときだけ入次数を減らします。
    """

    def __init__(self, n: int):
        self.n = n
        self.graph = [set() for _ in range(n)]
        self.indegree = [0] * n
        self.edge_count = defaultdict(int)

    def add_edge(self, u: int, v: int) -> None:
        """u -> v を1本追加します。"""
        key = (u, v)
        if self.edge_count[key] == 0:
            self.graph[u].add(v)
            self.indegree[v] += 1
        self.edge_count[key] += 1

    def remove_edge(self, u: int, v: int) -> bool:
        """
        u -> v を1本削除します。
        辺が存在しない場合は False、削除できた場合は True を返します。
        """
        key = (u, v)
        if self.edge_count[key] == 0:
            return False

        self.edge_count[key] -= 1
        if self.edge_count[key] == 0:
            self.graph[u].remove(v)
            self.indegree[v] -= 1
        return True

    def add_path(self, path: list[int]) -> None:
        """path[0] -> path[1] -> ... の辺を追加します。"""
        for u, v in zip(path, path[1:]):
            self.add_edge(u, v)

    def remove_path(self, path: list[int]) -> bool:
        """
        path[0] -> path[1] -> ... の辺を1本ずつ削除します。
        全ての辺を削除できた場合は True を返します。
        """
        removed_all = True
        for u, v in zip(path, path[1:]):
            removed_all &= self.remove_edge(u, v)
        return removed_all

    def has_edge(self, u: int, v: int) -> bool:
        """u -> v が1本以上存在するかを返します。"""
        return self.edge_count[(u, v)] > 0

    def edge_multiplicity(self, u: int, v: int) -> int:
        """u -> v の多重度を返します。"""
        return self.edge_count[(u, v)]

    def sort(self) -> list[int]:
        """通常のトポロジカルソートを返します。閉路がある場合は空配列を返します。"""
        indegree = self.indegree.copy()
        queue = deque(i for i in range(self.n) if indegree[i] == 0)
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

    def sort_lexicographical(self) -> list[int]:
        """辞書順最小のトポロジカルソートを返します。閉路がある場合は空配列を返します。"""
        indegree = self.indegree.copy()
        heap = []

        for i in range(self.n):
            if indegree[i] == 0:
                heappush(heap, i)

        order = []
        while heap:
            v = heappop(heap)
            order.append(v)
            for nv in self.graph[v]:
                indegree[nv] -= 1
                if indegree[nv] == 0:
                    heappush(heap, nv)

        if len(order) != self.n:
            return []
        return order

    def sort_unique(self) -> tuple[bool, list[int]]:
        """
        一意性判定付きトポロジカルソートを行います。

        戻り値:
            (一意であるか, 順序)

        閉路がある場合は (False, []) を返します。
        """
        indegree = self.indegree.copy()
        queue = deque(i for i in range(self.n) if indegree[i] == 0)
        order = []
        is_unique = True

        while queue:
            if len(queue) > 1:
                is_unique = False

            v = queue.popleft()
            order.append(v)
            for nv in self.graph[v]:
                indegree[nv] -= 1
                if indegree[nv] == 0:
                    queue.append(nv)

        if len(order) != self.n:
            return False, []
        return is_unique, order

    def is_dag(self) -> bool:
        """現在のグラフがDAG（有向非巡回グラフ）かを返します。"""
        return len(self.sort()) == self.n

    def order_to_rank(self, order: list[int]) -> list[int]:
        """
        order[何番目] = 頂点番号 から
        rank[頂点番号] = 何番目（1-indexed）を作ります。
        """
        if not order:
            return []

        rank = [0] * self.n
        for i, v in enumerate(order):
            rank[v] = i + 1
        return rank
