class DynamicUnionFind:
    def __init__(self, n):
        self.parent = list(range(n))  # 各ノードの親
        self.rank = [0] * n           # 各ノードのランク
        self.size = [1] * n          # 各連結成分のサイズ
        self.history = []            # 操作の履歴（rollback用）
        self.edges = set()           # 現在の辺集合

    def leader(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.leader(self.parent[x])  # 経路圧縮
        return self.parent[x]

    def merge(self, x, y):
        xr = self.leader(x)
        yr = self.leader(y)

        if xr == yr:
            return False

        # ランクを考慮してマージ
        if self.rank[xr] < self.rank[yr]:
            xr, yr = yr, xr

        self.history.append((yr, self.parent[yr], xr, self.size[xr]))

        self.parent[yr] = xr
        self.size[xr] += self.size[yr]

        if self.rank[xr] == self.rank[yr]:
            self.rank[xr] += 1

        self.edges.add((min(x, y), max(x, y)))
        return True

    def connected(self, x, y):
        return self.leader(x) == self.leader(y)

    def rollback(self):
        if not self.history:
            return False

        yr, old_parent, xr, old_size = self.history.pop()

        self.parent[yr] = old_parent
        self.size[xr] = old_size

        if self.rank[xr] > self.rank[yr]:
            self.rank[xr] -= 1

        return True

    def cut(self, x, y):
        # Ensure the edge exists
        edge = (min(x, y), max(x, y))
        if edge not in self.edges:
            return False

        self.edges.remove(edge)

        # Rollback until the edge is effectively removed
        while self.history:
            yr, old_parent, xr, old_size = self.history[-1]
            if (self.leader(x) != self.leader(y)):
                break
            self.rollback()

        return True

    def size_of(self, x):
        # Return the size of the connected component containing x
        return self.size[self.leader(x)]


N, M, E = [int(l) for l in input().split()]
duf = DynamicUnionFind(N + M)
for m in range(M - 1):
    duf.merge(N + m, N + m + 1)
UV = []
for e in range(E):
    u, v = [int(l) - 1 for l in input().split()]
    duf.merge(u, v)
    UV.append([u, v])
Q = int(input())
for q in range(Q):
    x = int(input()) - 1
    u, v = UV[x]
    duf.cut(u, v)
    print(duf.size_of(N) - M + 1)
