class SmallConv:
    """小規模な畳み込みを対象としたもの"""
    @staticmethod
    def conv(A: list[int], B: list[int], maxPow: int=10**10, MOD: int=998244353) -> list[int]:
        N = len(A) + len(B) - 1
        result = []
        for n in range(N):
            if n > maxPow:
                break
            tmp = 0
            for i in range(n+1):
                j = n - i
                if i >= len(A):
                    break
                if j >= len(B):
                    continue
                tmp = (tmp + A[i] * B[j]) % MOD
            result.append(tmp)
        return result

MOD = 998244353
L = 1000
frc = [1]
frc_r = [1]
c = 1
for i in range(1, L):
    c *= i
    frc.append(c)
    frc_r.append(pow(c, MOD-2, MOD))

N, M = map(int, input().split())
result = [1]
for i in range(1, M+1):
    result = SmallConv.conv(result, frc_r[:i+1], N + 1)
print(0 if len(result) <= N else (result[N] * frc[N]) % MOD)
