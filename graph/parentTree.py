class ParentTree:
    """
    P[v] < v が保証された根付き木用クラス（0-indexed）。

    P[root] = -1 とする。
    例:
        P = [-1, 0, 0, 1, 1, 3]
    """

    def __init__(self, P: list[int]):
        self.n = len(P)
        self.P = list(P)
        self.root = 0

        if self.n == 0:
            raise ValueError("頂点数は1以上である必要があります")
        if self.P[0] != -1:
            raise ValueError("P[0] は -1 である必要があります")

        self.depth = [0] * self.n
        for v in range(1, self.n):
            p = self.P[v]
            if not 0 <= p < v:
                raise ValueError("各 v > 0 について 0 <= P[v] < v が必要です")
            self.depth[v] = self.depth[p] + 1

    def parent(self, v: int) -> int:
        """v の親。根なら -1。"""
        return self.P[v]

    def kth_ancestor(self, v: int, k: int) -> int:
        """v から k 個上の祖先。根より上に行く場合は -1。O(k)。"""
        while k and v != -1:
            v = self.P[v]
            k -= 1
        return v

    def lca(self, u: int, v: int) -> int:
        """u, v の最近共通祖先。O(depth)。"""
        du = self.depth[u]
        dv = self.depth[v]

        while du > dv:
            u = self.P[u]
            du -= 1

        while dv > du:
            v = self.P[v]
            dv -= 1

        while u != v:
            u = self.P[u]
            v = self.P[v]

        return u

    def dist(self, u: int, v: int) -> int:
        """u-v 間の辺数。"""
        w = self.lca(u, v)
        return self.depth[u] + self.depth[v] - 2 * self.depth[w]

    def is_ancestor(self, u: int, v: int) -> bool:
        """u が v の祖先か。自分自身も祖先とみなす。O(depth)。"""
        if self.depth[u] > self.depth[v]:
            return False
        d = self.depth[v] - self.depth[u]
        return self.kth_ancestor(v, d) == u

    def path_to_ancestor(self, v: int, anc: int) -> list[int]:
        """v -> anc のパス。anc が祖先であることを仮定。両端を含む。"""
        res = []
        while v != anc:
            res.append(v)
            v = self.P[v]
        res.append(anc)
        return res

    def path(self, u: int, v: int) -> list[int]:
        """u -> v のパスを頂点列として返す。O(パス長)。"""
        w = self.lca(u, v)

        left = []
        while u != w:
            left.append(u)
            u = self.P[u]
        left.append(w)

        right = []
        while v != w:
            right.append(v)
            v = self.P[v]

        left.extend(reversed(right))
        return left

    def children(self) -> list[list[int]]:
        """子リストを構築して返す。O(N)。"""
        graph = [[] for _ in range(self.n)]
        for v in range(1, self.n):
            graph[self.P[v]].append(v)
        return graph
