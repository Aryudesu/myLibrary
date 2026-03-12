from dataclasses import dataclass
@dataclass
class Item:
    """ナップサック問題用クラス"""
    weight: int
    value: int

    def __repr__(self):
        return f"(Weight:{self.weight}, Value:{self.value})"

def valueKeyKnapsack(items: list[Item], W: int, INF: int = 10 ** 18)->int:
    """価値をキーとしてナップサック問題を計算します"""
    V = sum(item.value for item in items)
    dp = [INF] * (V + 1)
    dp[0] = 0
    for item in items:
        for v in range(V - item.value, -1, -1):
            if dp[v] == INF: continue
            dp[v + item.value] = min(dp[v + item.value], dp[v] + item.weight)
    return max(v for v in range(V + 1) if dp[v] <= W)


N, W = map(int, input().split())
WV = []
for n in range(N):
    w, v = map(int, input().split())
    WV.append(Item(w, v))
print(valueKeyKnapsack(WV, W))
