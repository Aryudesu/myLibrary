from collections import defaultdict

def count_subsequence_occurrences(A: list[int], P: list[int], mod: int = 10**9 + 7) -> int:
    """AからPを部分列として取り出す方法の個数をmodで計算"""
    K = len(P)
    pos = defaultdict(list)
    for i in range(K - 1, -1, -1):
        pos[P[i]].append(i)

    dp = [0] * K
    for a in A:
        for i in pos[a]:
            if i == 0:
                dp[0] = (dp[0] + 1) % mod
            else:
                dp[i] = (dp[i] + dp[i - 1]) % mod
    return dp[-1]


# AWC0028E
N, K = map(int, input().split())
A = list(map(int, input().split()))
P = list(map(int, input().split()))
print(count_subsequence_occurrences(A, P))
