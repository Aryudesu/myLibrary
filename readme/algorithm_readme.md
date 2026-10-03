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

## treeMo.py

`TreeMo`

木上のパスクエリを Mo's Algorithm で処理する。

- 各頂点を行きがけ・帰りがけに記録する長さ `2N` の Euler Tour を構築
- 区間内で奇数回登場する頂点を現在集合として管理
- LCA を一時的に追加することで任意の `s-t` パスを表現
- `addVertex` / `removeVertex` / `getAnswer(queryIndex)` を問題ごとに差し替えて利用

前処理は `O(N log N)`。Mo 部分は add/remove が `O(F)` のとき、おおむね `O(N sqrt(Q) F + Q log N)`。

## treeMoInline.py

`TreeMoInline`

Pythonで木上Moのホットループを問題側へ直書きしたい場合の軽量版。

- Euler Tour
- `tin / tout`
- LCA
- `(s, t)` から `(l, r, lca, queryIndex)` への変換
- Mo順へのクエリ整列

までをライブラリ側で行い、`add/remove/getAnswer` のコールバック呼び出しは行わない。

`getOrderedQueries()` で並べ替え済みクエリを取得し、区間伸縮・toggle・回答処理を問題側にベタ書きすることで、Pythonの関数呼び出しオーバーヘッドを減らせる。

通常版 `TreeMo` が書きやすさ優先、こちらは速度優先。

## hilbertMo.py

`hilbertOrder(x, y, bits)` / `sortMoQueriesHilbert(queries, maxCoord)`

Mo's Algorithm のクエリ `(l, r)` を Hilbert order で並べる補助関数。

`TreeMoInline` と組み合わせる場合は、

```python
ordered = sortMoQueriesHilbert(tm.queries, len(tm.euler))
```

として利用する。

通常のブロック分割 Mo より L/R の総移動量が減る場合があるが、
Hilbert index の計算自体にもコストがあるため、常に高速になるとは限らない。

