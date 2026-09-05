from dataclasses import dataclass
@dataclass
class Item:
    """ナップサック問題用クラス"""
    weight: int
    value: int

    def __repr__(self):
        return f"(Weight:{self.weight}, Value:{self.value})"


def unboundedWeightKeyKnapsack(items: list[Item], WMax: int, INF: int = 10 ** 18)->int:
    """重さをキーとして個数制限なしナップサック問題を計算します"""
    dp = [-INF] * (WMax + 1)
    dp[0] = 0
    for item in items:
        for w in range(WMax - item.weight + 1):
            if dp[w] == -INF: continue
            if w + item.weight > WMax: continue
            dp[w + item.weight] = max(dp[w + item.weight], dp[w] + item.value)
    return max(dp)

N, M, K = map(int, input().split())
items = []
for n in range(N):
    c, t, p = map(int, input().split())
    items.append(Item(t, p-c))
print(unboundedWeightKeyKnapsack(items, K) * M)
