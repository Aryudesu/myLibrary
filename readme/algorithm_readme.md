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
