# dp

動的計画法、および DP と同じ形の問題を高速に解くアルゴリズムをまとめる。

## subarraySum.py

- `maxSubarraySum(A, allowEmpty=False)`
  - 最大連続部分列和を Kadane 法で `O(N)` で求める。
- `minSubarraySum(A, allowEmpty=False)`
  - 最小連続部分列和を `O(N)` で求める。

`allowEmpty=True` の場合は空区間を許す。

## nonAdjacentKSum.py

- `minNonAdjacentKSum(A, K)`
  - 隣り合わない要素をちょうど `K` 個選ぶときの最小和。
- `maxNonAdjacentKSum(A, K)`
  - 隣り合わない要素をちょうど `K` 個選ぶときの最大和。

heap と双方向連結リストによる後悔貪欲を用い、計算量は `O((N + K) log N)`。

## bitsetSubsetSum.py

- `BitsetSubsetSum(max_sum=None)`: 非負整数の部分和の到達可能性を Python の整数のビットで高速に管理。
  - `add(x)`: 非負整数 `x` を1個追加する。
  - `contains(s)` / `s in dp`: 部分和 `s` が作れるか。
  - `max_leq(x)`: `x` 以下で作れる最大の部分和（なければ `None`）。
  - `min_geq(x)`: `x` 以上で作れる最小の部分和（なければ `None`）。
  - `max_sum` を指定するとその値を超える部分和を捨て、メモリと時間を節約できる。ただし問い合わせも保存範囲内のみ。削除・通り数計算には対応しない。

例（AWC0201 E、2人の荷物の重量差の最小値）:

```python
S = sum(A)
dp = BitsetSubsetSum(S // 2)
for a in A:
    dp.add(a)
best = dp.max_leq(S // 2)
print(S - 2 * best)
```


## tspBitDP.py

- `TSPBitDP(dist)`: 距離行列から巡回セールスマン問題をBitDPで解く。
  - `dist[i][j]`: 頂点 `i` → `j` の移動コスト（非対称でも可）。
  - `solve(start_cost, end_cost=None)`: 全頂点を訪問する最小コスト。
  - `start_cost[i]`: 始点から最初の頂点 `i` へのコスト。
  - `end_cost[i]`: 最後の頂点 `i` から終点へのコスト。省略時は終点自由。
  - 頂点数0なら0を返す。始点から終点への直接移動コストは含まない。
  - 時間 `O(N^2 2^N)`、空間 `O(N 2^N)`。頂点数が小さい場合向け。

例（AWC0202 E、配達先を全訪問して原点に戻る）:

```python
from dp.tspBitDP import TSPBitDP

N, M, K = map(int, input().split())
RC = [tuple(int(x) - 1 for x in input().split()) for _ in range(K)]

dist = [
    [abs(r1 - r2) + abs(c1 - c2) for r2, c2 in RC]
    for r1, c1 in RC
]
start_cost = [r + c for r, c in RC]

print(TSPBitDP(dist).solve(start_cost, start_cost))
```
