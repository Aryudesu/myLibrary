class OsaKMethod:
    def __init__(self, n: int):
        self.spf = list(range(n))
        for p in range(2, n):
            if p * p >= n:
                break
            if self.spf[p] != p:
                continue
            for i in range(p * p, n, p):
                if self.spf[i] == i:
                    self.spf[i] = p

    def factorize(self, n: int):
        res = []
        while n > 1:
            p = self.spf[n]
            c = 0
            while n % p == 0:
                n //= p
                c += 1
            res.append((p, c))
        return res

    def divisors(self, n: int):
        res = [1]
        for p, c in self.factorize(n):
            cur = []
            mul = 1
            for _ in range(c + 1):
                for x in res:
                    cur.append(x * mul)
                mul *= p
            res = cur
        return res

def calc(data: dict[int, int])->int:
    osak = OsaKMethod(10**6 + 5)
    resData = [0] * (10**6 + 5)
    result = 0
    cdf = osak.divisors
    for a, n in data.items():
        for d in cdf(a):
            resData[d] += d * n
            result = max(result, resData[d])
    return result

N = int(input())
A = list(map(int, input().split()))
data = dict()
for a in A:
    data[a] = data.get(a, 0) + 1
print(calc(data))
