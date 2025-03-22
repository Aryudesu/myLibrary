from collections import defaultdict


class HLDecomposition:
    def __init__(self, graph: dict, root=1):
        self.graph = graph
        self.n = len(graph)
        self.root = root

        self.parent = {v: None for v in graph}
        self.depth = {v: 0 for v in graph}
        self.subtree_size = {v: 1 for v in graph}
        self.head = {v: v for v in graph}
        self.heavy_child = {v: None for v in graph}
        self.euler = []
        self.pos = {}

        self._dfs_size(root)
        self._dfs_hld(root)

    def _dfs_size(self, v):
        max_size = 0
        for to in self.graph[v]:
            if to == self.parent[v]:
                continue
            self.parent[to] = v
            self.depth[to] = self.depth[v] + 1
            self._dfs_size(to)
            self.subtree_size[v] += self.subtree_size[to]
            if self.subtree_size[to] > max_size:
                max_size = self.subtree_size[to]
                self.heavy_child[v] = to

    def _dfs_hld(self, v, h=None):
        if h is None:
            h = v
        self.head[v] = h
        self.pos[v] = len(self.euler)
        self.euler.append(v)

        if self.heavy_child[v] is not None:
            self._dfs_hld(self.heavy_child[v], h)

        for to in self.graph[v]:
            if to != self.parent[v] and to != self.heavy_child[v]:
                self._dfs_hld(to)


# 使用例
graph = defaultdict(set)
graph[1].update([2, 3])
graph[2].update([1, 4, 5])
graph[3].update([1, 6, 7])
graph[4].update([2])
graph[5].update([2])
graph[6].update([3])
graph[7].update([3])

hl = HLDecomposition(graph)
print("Euler Tour:", hl.euler)
print("Positions:", hl.pos)
print("Heads:", hl.head)
