class dsu:
    def __init__(self, n=0) -> None:
        self.__n = n
        self.__parent_or_size = [-1] * n

    def merge(self, a, b):
        assert 0 <= a and a < self.__n
        assert 0 <= b and b < self.__n
        x = self.leader(a)
        y = self.leader(b)
        if x == y:
            return x
        if -self.__parent_or_size[x] < -self.__parent_or_size[y]:
            x, y = y, x
        self.__parent_or_size[x] += self.__parent_or_size[y]
        self.__parent_or_size[y] = x
        return x

    def some(self, a, b):
        assert 0 <= a and a < self.__n
        assert 0 <= b and b < self.__n
        return self.leader(a) == self.leader(b)

    def leader(self, a):
        assert 0 <= a and a < self.__n
        if self.__parent_or_size[a] < 0:
            return a
        self.__parent_or_size[a] = self.leader(self.__parent_or_size[a])
        return self.__parent_or_size[a]

    def size(self, a):
        assert 0 <= a and a < self.__n
        return -self.__parent_or_size[self.leader(a)]

    def groups(self):
        leader_buf = [self.leader(i) for i in range(self.__n)]
        result = [[] for i in range(self.__n)]
        for i in range(self.__n):
            result[leader_buf[i]].append(i)
        return list(filter(lambda r: r, result))


N, Q = [int(l) for l in input().split()]
dt = dsu(N)
result = []
for q in range(Q):
    t, u, v = [int(l) for l in input().split()]
    if t == 0:
        dt.merge(u, v)
    elif t == 1:
        result.append(1 if dt.some(u, v) else 0)

for r in result:
    print(r)
