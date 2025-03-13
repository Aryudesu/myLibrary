from collections import defaultdict

from sortedcontainers import SortedSet


class Mex:
    def __init__(self, m=0, n=2 * (10**5)):
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
        self.count[num] -= 1
        if self.count[num] == 0:
            self.data.discard(num)
            self.mexData.add(num)

    def change(self, a, b):
        self.discard(a)
        self.add(b)

    def getMex(self):
        return self.mexData[0]


N, Q = [int(l) for l in input().split()]
A = [int(l) for l in input().split()]
mex = Mex()
for a in A:
    mex.add(a)
for q in range(Q):
    i, x = [int(l) for l in input().split()]
    b = A[i - 1]
    A[i - 1] = x
    mex.change(b, x)
    print(mex.getMex())
