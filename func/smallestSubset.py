from heapq import heappop, heappush

def smallestSubset(S: str, K: int):
    """Sの部分列で辞書順最小の長さKのものを取得"""
    N = len(S)
    data = []
    prev = -1
    result = []
    for i in range(N):
        heappush(data, (S[i], i))
        if i < N - K:
            continue
        while True:
            c, j = heappop(data)
            if prev > j:
                continue
            prev = j
            result.append(c)
            break
    return "".join(result)

# === 競プロ典型006
N, K = [int(l) for l in input().split()]
S = input()
print(smallestSubset(S, K))
