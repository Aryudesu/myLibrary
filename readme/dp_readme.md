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
