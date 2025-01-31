from atcoder.dsu import DSU


class MonoidUnionFind(DSU):

    def __init__(self, n, func, initialize):
        super.__init__(n)
        self.func = func
        self.total = initialize

    def union(self, a: int, b: int):
        assert 0 <= a < self._n
        assert 0 <= b < self._n

        x = self.leader(a)
        y = self.leader(b)
        if x == y:
            return True

        new_data = self.func(self.total.get(x), self.total.get(y))
        self.merge(a, b)
        new_leader = self.leader(a)
        self.total[new_leader] = new_data

        return False

    def get_total(self, a: int):
        return self.total.get(self.leader(a))


N, Q = [int(l) for l in input().split()]
muf = MonoidUnionFind(N)
for _ in range(Q):
    query = [int(l) for l in input().split()]
    if query[0] == 1:
        q, x, c = query
    elif query[0] == 2:
        q, c = query
