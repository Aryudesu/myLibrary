# graph

## graph/graph

二分グラフかを判定する

## graph/tree

重み付き無向木の基本クラス。

- `add_edge(u, v, weight=1)` で無重み木・重み付き木を統一
- 頂点コストの保持
- 始点から各頂点への重み付き距離
- 最遠点取得
- 木の重み付き直径

Euler Tour や LCA が不要な場合はこちらを使う。

## graph/euler_tour

`Tree` を継承した Euler Tour + RMQ による根付き木ユーティリティ。

- LCA
- 祖先判定
- 部分木サイズ
- 2頂点間の辺数
- 2頂点間の重み付き距離
- 根からの重み付き距離
- 静的な頂点コストの部分木和・パス和
- 静的な辺コストの部分木和

辺追加などの基本機能は `Tree` から継承する。

## graph/functionalGraph/functionalGraph

Functional Graph 用クラス。

- サイクル分解
- 各頂点からサイクルまでの距離
- サイクルへの入口
- `jump(v, k)` / `kth(start, k)`
- 到達可能性・最短遷移回数
- 弱連結成分判定
- サイクル列挙
- `orbit(start)` で最初の再訪までの軌道取得
- `distinct_orbit_size(v)`

基本構築は時間・メモリともに `O(N)`。
Doubling は木部分を途中までジャンプする必要が生じたときだけ遅延構築し、追加で `O(N log N)` の時間・メモリを使う。
サイクル情報や `distinct_orbit_size()` だけを使う場合は Doubling を構築しない。

旧 `functional.py` の始点固定解析機能もこのクラスへ統合済み。

## graph/parentTree

`P[v] < v` が保証された親配列形式の根付き木用クラス。

- 親取得
- k 個上の祖先
- LCA
- 距離
- 祖先判定
- パス復元
- 子リスト構築

Functional Graph とは用途が異なるため別クラスとして管理する。

## graph/topology_sort

トポロジカルソート。

- 通常のトポロジカルソート
- 辞書順最小のトポロジカルソート
- 順序の一意性判定
- DAG判定
- 多重辺対応
- 辺・パスの追加削除
