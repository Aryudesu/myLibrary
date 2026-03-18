from bisect import bisect_left

class MissingOrderQuery:
    def __init__(self, A):
        self.A = sorted(A)
        self.B = [a - i for i, a in enumerate(self.A)]

    def kth_missing_ge(self, X, Y):
        p = bisect_left(self.A, X)
        idx = bisect_left(self.B, X - p + Y, p)
        return X + Y - 1 + (idx - p)

# ABC440D
N, Q = map(int, input().split())
A = list(map(int, input().split()))
mnq = MissingOrderQuery(A)
for _ in range(Q):
    x, y = map(int, input().split())
    print(mnq.kth_missing_ge(x, y))
