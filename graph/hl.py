from atcoder.fenwicktree import FenwickTree
import sys
sys.setrecursionlimit(1_000_000)
input = sys.stdin.readline


class HLDecomposition:
    """
    1-indexed 木の Heavy-Light Decomposition

    G: 隣接リスト (1..N)
    root: 根

    フィールド:
      parent[v], depth[v], heavy[v], head[v], pos[v], inv[pos], subtree_size[v]

    主なメソッド:
      lca(u, v)
      dist(u, v)            # 辺数としての距離（今回は不要）
      subtree_range(v)      # 部分木 [l, r]（今回は不要）
    """

    def __init__(self, G, root=1):
        self.n = len(G) - 1  # G は 1..N を使う想定
        self.G = G
        self.root = root

        N = self.n
        self.parent = [0] * (N + 1)
        self.depth = [0] * (N + 1)
        self.subtree_size = [0] * (N + 1)
        self.heavy = [-1] * (N + 1)
        self.head = [0] * (N + 1)
        self.pos = [0] * (N + 1)   # 頂点 → 基底配列 index (0-indexed)
        self.inv = [0] * N         # 基底配列 index → 頂点

        # 1: 部分木サイズ & heavy child 計算
        self._dfs_size(root, 0)
        # 2: heavy path ごとに head と pos を張る
        cur = 0
        self._dfs_hld(root, root, cur)

    def _dfs_size(self, v, p):
        self.parent[v] = p
        self.subtree_size[v] = 1
        max_size = 0
        for to in self.G[v]:
            if to == p:
                continue
            self.depth[to] = self.depth[v] + 1
            self._dfs_size(to, v)
            sz = self.subtree_size[to]
            self.subtree_size[v] += sz
            if sz > max_size:
                max_size = sz
                self.heavy[v] = to

    def _dfs_hld(self, v, h, cur):
        """ heavy path ごとに head と pos を割り当てる """
        self.head[v] = h
        self.pos[v] = cur
        self.inv[cur] = v
        cur += 1
        # heavy child を同じ鎖で伸ばす
        if self.heavy[v] != -1:
            cur = self._dfs_hld(self.heavy[v], h, cur)
        # その他のchildは新しい鎖の head になる
        for to in self.G[v]:
            if to == self.parent[v] or to == self.heavy[v]:
                continue
            cur = self._dfs_hld(to, to, cur)

        return cur

    def lca(self, u, v):
        while self.head[u] != self.head[v]:
            if self.depth[self.head[u]] > self.depth[self.head[v]]:
                u = self.parent[self.head[u]]
            else:
                v = self.parent[self.head[v]]
        return u if self.depth[u] < self.depth[v] else v

    def dist(self, u, v):
        """ 辺数としての距離 """
        w = self.lca(u, v)
        return self.depth[u] + self.depth[v] - 2 * self.depth[w]

    def subtree_range(self, v):
        """
        頂点 v の部分木が基底配列上で占める区間 [l, r] を返す
        頂点に値を乗せるタイプのときに使う
        """
        l = self.pos[v]
        r = l + self.subtree_size[v] - 1
        return l, r


def sum_up(hl, bit_up: FenwickTree, u, anc):
    """
    u から anc (祖先) まで木を「登る」部分のコストの合計
    辺のコストは子頂点 pos[child] に載っている前提で、
    子→親方向のコスト (w_up) を Fenwick に載せている。
    """
    parent = hl.parent
    head = hl.head
    pos = hl.pos

    res = 0
    while head[u] != head[anc]:
        h = head[u]
        # 鎖 head[h]..u まで全部「登る」から、その区間の w_up を足す
        res += bit_up.sum(pos[h], pos[u]+1)
        u = parent[h]

    # 同じ鎖になったら anc 直下の子から u まで
    if u != anc:
        res += bit_up.sum(pos[anc] + 1, pos[u]+1)
    return res


def sum_down(hl, bit_down, v, anc):
    """
    anc から v まで木を「下る」部分のコストの合計
    辺のコストは子頂点 pos[child] に載っている前提で、
    親→子方向のコスト (w_down) を Fenwick に載せている。
    """
    parent = hl.parent
    head = hl.head
    pos = hl.pos

    u = v
    res = 0
    while head[u] != head[anc]:
        h = head[u]
        res += bit_down.sum(pos[h], pos[u]+1)
        u = parent[h]

    if u != anc:
        res += bit_down.sum(pos[anc] + 1, pos[u]+1)
    return res


def main():
    N, M = map(int, input().split())

    # 隣接リスト（1..N）
    G = [[] for _ in range(N + 1)]
    # 辺の端点 (常に p < q)
    edges = [None] * (N)  # 1..N-1 を使う

    for i in range(1, N):
        p, q = map(int, input().split())
        if p > q:
            p, q = q, p
        edges[i] = (p, q)
        G[p].append(q)
        G[q].append(p)

    # HL 分解を構築（根は 1 とする）
    hl = HLDecomposition(G, root=1)
    parent = hl.parent
    pos = hl.pos

    # 各辺 i に対応する「子側」の頂点 child[i]
    child = [0] * (N)

    # 生の up / down（小さい→大きい, 大きい→小さい）
    up_raw = [0] * (N)
    down_raw = [0] * (N)

    # 木の方向での up/down
    # w_up[i]   : 子 -> 親 のコスト
    # w_down[i] : 親 -> 子 のコスト
    w_up = [0] * (N)
    w_down = [0] * (N)

    bit_up = FenwickTree(N+1)
    bit_down = FenwickTree(N+1)

    # 初期状態：全ての高速道路で up = down = 1
    for i in range(1, N):
        up_raw[i] = 1
        down_raw[i] = 1
        a, b = edges[i]  # a < b

        # 親子判定
        if parent[a] == b:
            parent_node = b
            child_node = a
        elif parent[b] == a:
            parent_node = a
            child_node = b
        else:
            # 木なのでどちらかが必ず親
            raise RuntimeError("edge does not connect parent-child")

        child[i] = child_node

        small, large = a, b  # small < large

        # 親->子 のとき、番号の向きがどうなっているかで使うコストが変わる
        if parent_node == small:
            # 親=small, 子=large
            # 親→子 は small->large ⇒ up_raw
            # 子→親 は large->small ⇒ down_raw
            down = up_raw[i]   # 親→子
            up = down_raw[i]   # 子→親
        else:
            # 親=large, 子=small
            # 親→子 は large->small ⇒ down_raw
            # 子→親 は small->large ⇒ up_raw
            down = down_raw[i]
            up = up_raw[i]

        w_down[i] = down
        w_up[i] = up

        # Fenwick に登録（child_node の位置に辺コストを載せる）
        idx = pos[child_node]
        bit_down.add(idx, down)
        bit_up.add(idx, up)

    # クエリ処理
    out_lines = []
    for _ in range(M):
        tmp = input().split()
        if not tmp:
            continue
        if tmp[0] == 'I':
            # 更新: I r s t
            _, r_str, s_str, t_str = tmp
            r = int(r_str)
            s = int(s_str)
            t = int(t_str)

            up_raw[r] = s
            down_raw[r] = t

            a, b = edges[r]
            c = child[r]
            parent_node = parent[c]
            small, large = a, b  # small < large

            # 新しい木方向コストを計算
            if parent_node == small:
                down = s  # 親=small -> 子=large は small->large
                up = t    # 子=large -> 親=small は large->small
            else:
                down = t  # 親=large -> 子=small は large->small
                up = s    # 子=small -> 親=large は small->large

            # Fenwick を差分更新
            idx = pos[c]
            delta_down = down - w_down[r]
            delta_up = up - w_up[r]
            if delta_down != 0:
                bit_down.add(idx, delta_down)
            if delta_up != 0:
                bit_up.add(idx, delta_up)

            w_down[r] = down
            w_up[r] = up

        else:
            # 質問: Q x y
            _, x_str, y_str = tmp
            x = int(x_str)
            y = int(y_str)
            l = hl.lca(x, y)

            ans = sum_up(hl, bit_up, x, l) + sum_down(hl, bit_down, y, l)
            out_lines.append(str(ans))

    print("\n".join(out_lines))


if __name__ == "__main__":
    main()
