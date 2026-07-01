class DoublingLCA:
    EDGE = 0
    NODE = 1

    def __init__(self, n, graph, op, e, values=None, mode=EDGE, root=0):
        """
        graph:
          EDGE: graph[v] = [(to, cost), ...]
          NODE: graph[v] = [to, ...] でも [(to, cost), ...] でも可

        values:
          NODE のとき node_values
          EDGE のとき不要
        """
        self.n = n
        self.LOG = max(1, n.bit_length())
        self.op = op
        self.e = e
        self.mode = mode
        self.values = values

        self.depth = [-1] * n
        self.parent = [[-1] * n for _ in range(self.LOG)]
        self.data = [[e] * n for _ in range(self.LOG)]

        self.depth[root] = 0
        stack = [(root, -1, e)]

        while stack:
            v, p, w = stack.pop()
            self.parent[0][v] = p

            if mode == DoublingLCA.EDGE:
                self.data[0][v] = w
            else:
                self.data[0][v] = values[v]

            for item in graph[v]:
                if isinstance(item, tuple):
                    to = item[0]
                    cost = item[1]
                else:
                    to = item
                    cost = e

                if to == p:
                    continue

                self.depth[to] = self.depth[v] + 1
                stack.append((to, v, cost))

        for k in range(self.LOG - 1):
            for v in range(n):
                p = self.parent[k][v]
                if p == -1:
                    self.parent[k + 1][v] = -1
                    self.data[k + 1][v] = self.data[k][v]
                else:
                    self.parent[k + 1][v] = self.parent[k][p]
                    self.data[k + 1][v] = op(self.data[k][v], self.data[k][p])

    def kth_ancestor(self, v, k):
        for i in range(self.LOG):
            if k >> i & 1:
                v = self.parent[i][v]
                if v == -1:
                    return -1
        return v

    def lca(self, u, v):
        if self.depth[u] < self.depth[v]:
            u, v = v, u

        u = self.kth_ancestor(u, self.depth[u] - self.depth[v])

        if u == v:
            return u

        for k in reversed(range(self.LOG)):
            if self.parent[k][u] != self.parent[k][v]:
                u = self.parent[k][u]
                v = self.parent[k][v]

        return self.parent[0][u]

    def prod(self, u, v):
        """
        EDGE: u-v パス上の辺を集約
        NODE: u-v パス上の頂点を集約
        """
        op = self.op
        res = self.e

        if self.depth[u] < self.depth[v]:
            u, v = v, u

        diff = self.depth[u] - self.depth[v]

        for k in range(self.LOG):
            if diff >> k & 1:
                res = op(res, self.data[k][u])
                u = self.parent[k][u]

        if u == v:
            if self.mode == DoublingLCA.NODE:
                res = op(res, self.data[0][u])
            return res

        for k in reversed(range(self.LOG)):
            if self.parent[k][u] != self.parent[k][v]:
                res = op(res, self.data[k][u])
                res = op(res, self.data[k][v])
                u = self.parent[k][u]
                v = self.parent[k][v]

        # 最後に u, v から LCA へ上がる1辺/1頂点ぶん
        if self.mode == DoublingLCA.EDGE:
            res = op(res, self.data[0][u])
            res = op(res, self.data[0][v])
        else:
            res = op(res, self.data[0][u])
            res = op(res, self.data[0][v])
            l = self.parent[0][u]
            res = op(res, self.data[0][l])

        return res

    def dist(self, u, v):
        l = self.lca(u, v)
        return self.depth[u] + self.depth[v] - 2 * self.depth[l]

    def jump(self, u, v, k):
        """
        u から v へ k 辺進んだ頂点
        """
        l = self.lca(u, v)
        du = self.depth[u] - self.depth[l]
        d = self.dist(u, v)

        if k > d:
            return -1
        if k <= du:
            return self.kth_ancestor(u, k)
        return self.kth_ancestor(v, d - k)
