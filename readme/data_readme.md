# data

データ形式について

## unionFind/RollBackUnionFind

ロールバック可能なUnionFind

## arrayUtility

配列に関する操作とか

## insertable_list

挿入可能なリスト

### InsertableList(A: list = [])

Aで初期化したデータを作成しInsertableListを作成します．

### insert(x, y)

xの後にyを挿入します

### delete(x)

要素xを削除します

### getArray()

配列を取得します

## queue

キューの挙動の実装

### Queue(A: list = [])

Aでデータの初期化を行いQueueを作成します

### queue(a)

データaを追加します

### dequeueL()

先頭のデータを取得し，削除します

### dequeueR()

末尾のデータを取得し，削除します

### getL()

先頭のデータの取得を行います

### getR()

末尾のデータの取得を行います

## run_length

ランレングス圧縮

### RunLengh()

RunLengthクラスの作成を行います．初期はデータは空です．

### insert(x, n)

データxをn個追加します

### deque(n)

先頭からn個データを取得します

### popData(n)

末尾からn個データを取得します

## trie_tree

Trie木

### Trie()

Trieクラスの作成を行います．

### insert(value)

文字列データの追加を行います．

### search(word)

指定の文字列が存在するかを判定します

### starts_with(prefix)

先頭一致でデータの取得を行います

## segmentTree/rangeAddRangeSum

`RangeAddRangeSum`

遅延セグメント木による区間加算・区間和取得。

- `range_add(l, r, x)` : 半開区間 `[l, r)` に `x` を加算
- `range_sum(l, r)` : 半開区間 `[l, r)` の総和
- `all_sum()` : 全体の総和
- `get(i)` : `i` 番目の値

構築 `O(N)`、更新・取得 `O(log N)`。

## occurrenceIndex.py

`OccurrenceIndex(A)`

静的配列の値ごとの出現位置を管理する。値は hashable、0-index、半開区間。

- `getPositions(x)`: 出現位置のタプル（未出現なら空）
- `count(l, r, x)`: 区間内の出現回数
- `prev(i, x)`: i 未満の最後の位置（なければ -1）
- `next(i, x)`: i より後の最初の位置（なければ N）
- `kth(l, r, x, k)`: 区間内の k 番目の位置（0-index、なければ -1）
- `countExactK(l, r, x, k)`: 区間内で x をちょうど k 個含む非空部分区間数（k=0 対応）

構築・空間 O(N)、位置一覧取得 O(1) 平均、二分探索 O(log N)、countExactK O(log N + f)（f は区間内の出現回数）。
