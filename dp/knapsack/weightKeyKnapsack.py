from dataclasses import dataclass
@dataclass
class Item:
    """ナップサック問題用クラス"""
    weight: int
    value: int

    def __repr__(self):
        return f"(Weight:{self.weight}, Value:{self.value})"


def weightKeyKnapsack(items: list[Item], W: int, INF: int = 10 ** 18)->int:
    """重さをキーにしてナップサック問題を計算します"""
    NEGINF = -INF
    dp = [NEGINF] * (W + 1)
    dp[0] = 0
    for item in items:
        for w in range(W-item.weight, -1, -1):
            if dp[w] == NEGINF:continue
            dp[w + item.weight] = max(dp[w + item.weight], dp[w] + item.value)
    return max(dp)

N, W = map(int, input().split())
WV = []
for n in range(N):
    w, v = map(int, input().split())
    WV.append(Item(w, v))
print(weightKeyKnapsack(WV, W))
