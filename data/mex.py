from collections import defaultdict

from sortedcontainers import SortedSet


class Mex:
    def __init__(self, m=0, n=2 * (10**6)):
        self.minNum = m
        self.maxNum = n
        self.count = defaultdict(lambda: 0)
        self.data = SortedSet()
        self.mexData = SortedSet()
        for i in range(m, n + 1 + 2):
            self.mexData.add(i)

    def add(self, num):
        if num < self.minNum:
            return
        if num > self.maxNum:
            return
        self.count[num] += 1
        if self.count[num] == 1:
            self.data.add(num)
            self.mexData.discard(num)

    def discard(self, num):
        if num < self.minNum:
            return
        if num > self.maxNum:
            return
        if self.count[num] > 0:
            self.count[num] -= 1
            if self.count[num] == 0:
                self.data.discard(num)
                self.mexData.add(num)

    def change(self, a, b):
        self.discard(a)
        self.add(b)

    def get_mex(self):
        return self.mexData[0]


# ABC194E

N, M = [int(l) for l in input().split()]
A = [int(l) for l in input().split()]
mex = Mex(0, 15 * (10**5))
for i in range(M):
    mex.add(A[i])
result = mex.get_mex()
for i in range(1, N - M + 1):
    mex.discard(A[i - 1])
    mex.add(A[i + M - 1])
    result = min(result, mex.get_mex())
print(result)
