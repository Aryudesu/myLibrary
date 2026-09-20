# algorithm

汎用アルゴリズムをまとめる。

## mo.py

`Mo`

静的配列に対するオフライン区間クエリを Mo's Algorithm で処理する。

## nearestGreater.py

`nearestGreaterIndices(A)`

各要素 `A[i]` について、

- 左側で最も近い `A[j] > A[i]` の index
- 右側で最も近い `A[j] > A[i]` の index

を単調スタックで一括して求める。

存在しない場合は、左側を `-1`、右側を `len(A)` とする。

計算量は `O(N)`。

## weightedDistanceSum1D.py

`weightedDistanceSum1D(W)`

各位置 `x` について、1次元上の重み付き距離和

`sum(W[i] * abs(i - x))`

を全ての `x` に対して求める。

隣の位置へ移動したときの距離和の差分を利用し、計算量は `O(N)`。

## dyadicDecompose.py

`dyadicDecompose(L, R)`

半開区間 `[L, R)` を、

- 長さが2の冪
- 開始位置がその長さの倍数

となる区間へ分解する。

bit DP、popcount、巨大整数区間などで、2冪境界に揃った区間へ分割したい場合に利用する。
