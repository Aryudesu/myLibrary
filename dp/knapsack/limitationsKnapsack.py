from dataclasses import dataclass
@dataclass
class LimitationsItem:
    """個数制限つきナップサック問題用クラス"""
    weight: int
    value: int
    count: int
    def __repr__(self):
        return f"(Weight:{self.weight}, Value:{self.value}, Count:{self.count})"

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

def limitationWeightKeyKnapsack(limitationsItems: list[LimitationsItem], W: int)->int:
    """重さをキーにして個数制限ナップサック問題を計算します"""
    items = []
    for lItem in limitationsItems:
        w, v, c = lItem.weight, lItem.value, lItem.count
        k = 1
        while c > 0:
            take = min(k, c)
            items.append(Item(w * take, v * take))
            c -= take
            k <<= 1
    return weightKeyKnapsack(items, W)

N, W = map(int, input().split())
WVC = []
for n in range(N):
    w, v, c = map(int, input().split())
    WVC.append(LimitationsItem(w, v, c))
print(limitationWeightKeyKnapsack(WVC, W))
