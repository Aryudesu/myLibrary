from collections import defaultdict

class SubsetSum:
    """重複を許す集合の部分和問題"""
    def __init__(self, MAX: int=5000, mod: int = 998244353):
        self.data = [0] * (MAX + 1)
        self.data[0] = 1
        self.max = MAX
        self.mod = mod
        self.nums = defaultdict(int)
    
    def add(self, m: int):
        """xを追加"""
        assert m > 0
        self.nums[m] += 1
        if m > self.max:
            return
        for i in range(self.max , m - 1, -1):
            self.data[i] += self.data[i-m]
            if self.data[i] >= self.mod:
                self.data[i] -= self.mod

    def remove(self, m: int):
        """xを削除"""
        assert self.nums[m] > 0
        self.nums[m] -= 1
        if m > self.max:
            return
        for i in range(m, self.max+1):
            self.data[i] -= self.data[i-m]
            if self.data[i] < 0:
                self.data[i] += self.mod

    def get(self, s: int) -> int:
        """sになる通り数を取得"""
        assert 0 <= s <= self.max
        return self.data[s]

# ====== ABC321F

Q, K = map(int, input().split())
ss = SubsetSum(K)
result = []
for _ in range(Q):
    q, n = input().split()
    n = int(n)
    if q == "+":
        ss.add(n)
    elif q == "-":
        ss.remove(n)
    else:
        raise Exception()
    result.append(ss.get(K))
for r in result:
    print(r)
