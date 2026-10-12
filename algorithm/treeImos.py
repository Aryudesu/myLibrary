class TreeImos:
    """根付き木の部分木・部分木の外側への加算をまとめて処理する。

    graph は 0-indexed の無向木。各辺は両方向に登録する。
    addSubtree(v, x): 頂点 v の部分木に x 加算
    addOutsideSubtree(v, x): 頂点 v の部分木以外に x 加算
    build(): 各頂点の累積値を返す

    初期化と build は O(N)、各 add は O(1)、追加空間 O(N)。
    非再帰 DFS を使うため、直線状の木でも再帰制限に依存しない。
    """

    def __init__(self, graph: list[list[int]], root: int = 0):
        n = len(graph)
        if n == 0 or not 0 <= root < n:
            raise ValueError("invalid root or empty graph")
        self.n = n
        self.root = root
        self.parent = [-2] * n
        self.parent[root] = -1
        self.order = [root]
        for v in self.order:
            for u in graph[v]:
                if u == self.parent[v]:
                    continue
                if self.parent[u] != -2:
                    raise ValueError("graph must be a tree")
                self.parent[u] = v
                self.order.append(u)
        if len(self.order) != n:
            raise ValueError("graph must be connected")
        self.subtreeSize = [1] * n
        for v in reversed(self.order[1:]):
            self.subtreeSize[self.parent[v]] += self.subtreeSize[v]
        self.diff = [0] * n

    def addSubtree(self, v: int, x: int) -> None:
        self.diff[v] += x

    def addOutsideSubtree(self, v: int, x: int) -> None:
        self.diff[self.root] += x
        self.diff[v] -= x

    def build(self) -> list[int]:
        result = self.diff.copy()
        for v in self.order[1:]:
            result[v] += result[self.parent[v]]
        return result
