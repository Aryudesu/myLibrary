class RootTree:
    """
    無向木を任意の根から根付き木に変換する（0-indexed）。
    graph[v] は隣接頂点、または (隣接頂点, 辺重み) のリスト。
    無重み辺の重みは1。連結な無向木を前提とする。
    構築 O(N)、空間 O(N)。
    """

    def __init__(self, graph, root=0):
        self.n = n = len(graph)
        if not 0 <= root < n:
            raise ValueError("invalid root")
        self.root = root
        self.parent = [-2] * n
        self.parent[root] = -1
        self.parentCost = [0] * n
        self.depth = [0] * n
        self.dist = [0] * n
        self.children = [[] for _ in range(n)]
        self.order = [root]

        for v in self.order:
            for edge in graph[v]:
                u, c = (edge, 1) if isinstance(edge, int) else edge
                if u == self.parent[v]:
                    continue
                if not 0 <= u < n or self.parent[u] != -2:
                    raise ValueError("graph must be a tree")
                self.parent[u] = v
                self.parentCost[u] = c
                self.depth[u] = self.depth[v] + 1
                self.dist[u] = self.dist[v] + c
                self.children[v].append(u)
                self.order.append(u)
        if len(self.order) != n:
            raise ValueError("graph must be connected")

    def topDown(self):
        """親から子への処理順（根を含む）。"""
        return iter(self.order)

    def bottomUp(self):
        """子から親への処理順（根を含む）。"""
        return reversed(self.order)


RootedTree = RootTree
