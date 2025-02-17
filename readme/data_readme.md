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
