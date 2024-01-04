class fenwickTree:
    __data = []
    def __sum(self, r):
        s = 0
        while r > 0:
            s += self.__data[r-1]
            r -= r & -r
        return s

    def __init__(self, n=0) -> None:
        self.__n = n
        self.__data = [0] * n

    def set(self, v):
        """配列を初期設定します"""
        n = len(v)
        for i in range(n):
            self.add(i, v[i])

    def add(self, p, x):
        """a[p] += xを行います"""
        assert 0 <= p and p < self.__n
        p += 1
        while p <= self.__n:
            self.__data[p-1] += x
            p += p & -p

    def sum(self, l, r):
        """a[l] + a[l+1] + ... + a[r - 1]を返却します"""
        assert 0 <= l and l <= r and r <= self.__n
        return self.__sum(r) - self.__sum(l)


N, Q = [int(l) for l in input().split()]
A = [int(l) for l in input().split()]
ft = fenwickTree(N)
ft.set(A)
result = []
for q in range(Q):
    X, Y, Z = [int(l)for l in input().split()]
    if X == 0:
        ft.add(Y, Z)
    elif X == 1:
        result.append(ft.sum(Y, Z))

for r in result:
    print(r)