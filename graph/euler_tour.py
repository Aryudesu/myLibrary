from graph.tree import Tree


class EulerTourTree(Tree):
    """
    Euler Tour + RMQ による根付き木ユーティリティ。

    Tree を継承しているため、辺追加や木の直径などの基本機能は Tree 側を使う。
    辺の重みを省略した場合は 1 として扱う。

    主な機能:
    - LCA
    - 祖先判定
    - 部分木サイズ
    - 2頂点間の辺数
    - 2頂点間の重み付き距離
    - 根からの重み付き距離
    - 静的な頂点コストの部分木和 / パス和
    - 静的な辺コストの部分木和
    """

    def __init__(self, n: int):
        super().__init__(n)
        self._built = False

    def add_edge(self, u: int, v: int, weight: int = 1) -> None:
        """無向辺 u-v を追加する。追加後は build() が必要になる。"""
        super().add_edge(u, v, weight)
        self._built = False

    def set_node_cost(self, costs: list[int]) -> None:
        """各頂点の静的コストを設定する。"""
        super().set_node_cost(costs)
        if self._built:
            self._build_cost_data()

    def build(self, root: int = 0) -> None:
        """root を根として Euler Tour・LCA用RMQ等を構築する。"""
        n = self.n
        if n == 0:
            self.root = -1
            self._built = True
            return

        self.root = root
        self.parent = [-1] * n
        self.depth = [0] * n
        self.root_dist = [0] * n
        self.parent_edge_weight = [0] * n
        self.tin = [-1] * n
        self.tout = [-1] * n
        self.subtree_size = [0] * n

        self.euler = []
        self.euler_depth = []
        self.first = [-1] * n

        order = []
        timer = 0

        # (vertex, parent, parent_edge_weight, state)
        # state=0: 入る, state=1: 出る, state=2: 子から戻る
        stack = [(root, -1, 0, 0)]

        while stack:
            v, p, w, state = stack.pop()

            if state == 0:
                self.parent[v] = p
                self.parent_edge_weight[v] = w

                if p != -1:
                    self.depth[v] = self.depth[p] + 1
                    self.root_dist[v] = self.root_dist[p] + w

                self.tin[v] = timer
                timer += 1
                order.append(v)

                self.first[v] = len(self.euler)
                self.euler.append(v)
                self.euler_depth.append(self.depth[v])

                stack.append((v, p, w, 1))

                children = [(to, cost) for to, cost in self.graph[v] if to != p]
                for to, cost in reversed(children):
                    stack.append((v, p, w, 2))
                    stack.append((to, v, cost, 0))

            elif state == 2:
                self.euler.append(v)
                self.euler_depth.append(self.depth[v])

            else:
                # preorder の半開区間 [tin[v], tout[v]) が部分木になる
                self.tout[v] = timer

        self._order = order

        self.subtree_size = [1] * n
        for v in reversed(order):
            p = self.parent[v]
            if p != -1:
                self.subtree_size[p] += self.subtree_size[v]

        self._build_rmq()
        self._built = True
        self._build_cost_data()

    def _build_rmq(self) -> None:
        """Euler列上のdepth最小位置を返す Sparse Table を構築する。"""
        m = len(self.euler)

        self._log = [0] * (m + 1)
        for i in range(2, m + 1):
            self._log[i] = self._log[i // 2] + 1

        self._st = [list(range(m))]
        k = 1
        while (1 << k) <= m:
            prev = self._st[-1]
            half = 1 << (k - 1)
            width = 1 << k
            row = [0] * (m - width + 1)

            for i in range(len(row)):
                left = prev[i]
                right = prev[i + half]
                row[i] = (
                    left
                    if self.euler_depth[left] <= self.euler_depth[right]
                    else right
                )

            self._st.append(row)
            k += 1

    def _build_cost_data(self) -> None:
        """静的な頂点コスト・辺コストに関する累積値を構築する。"""
        n = self.n
        self._root_node_cost = [0] * n

        for v in self._order:
            p = self.parent[v]
            if p == -1:
                self._root_node_cost[v] = self.node_cost[v]
            else:
                self._root_node_cost[v] = self._root_node_cost[p] + self.node_cost[v]

        self._subtree_node_cost = self.node_cost.copy()
        self._subtree_edge_cost = [0] * n

        for v in reversed(self._order):
            p = self.parent[v]
            if p != -1:
                self._subtree_node_cost[p] += self._subtree_node_cost[v]
                self._subtree_edge_cost[p] += (
                    self._subtree_edge_cost[v] + self.parent_edge_weight[v]
                )

    def _ensure_built(self) -> None:
        if not self._built:
            self.build(0)

    def get_lca(self, u: int, v: int) -> int:
        """u, v の最近共通祖先を返す。"""
        self._ensure_built()
        l = self.first[u]
        r = self.first[v]
        if l > r:
            l, r = r, l

        k = self._log[r - l + 1]
        left = self._st[k][l]
        right = self._st[k][r - (1 << k) + 1]
        index = (
            left
            if self.euler_depth[left] <= self.euler_depth[right]
            else right
        )
        return self.euler[index]

    def lca(self, u: int, v: int) -> int:
        """get_lca の別名。"""
        return self.get_lca(u, v)

    def is_ancestor(self, u: int, v: int) -> bool:
        """u が v の祖先であるか判定する。自分自身も祖先とみなす。"""
        self._ensure_built()
        return self.tin[u] <= self.tin[v] < self.tout[u]

    def get_subtree_size(self, v: int) -> int:
        """v を根とする部分木の頂点数を返す。"""
        self._ensure_built()
        return self.subtree_size[v]

    def get_path_length(self, u: int, v: int) -> int:
        """u-v パスの辺数を返す。辺の重みは考慮しない。"""
        self._ensure_built()
        a = self.get_lca(u, v)
        return self.depth[u] + self.depth[v] - 2 * self.depth[a]

    def get_distance(self, u: int, v: int) -> int:
        """u-v パスの辺重みの総和を返す。"""
        self._ensure_built()
        a = self.get_lca(u, v)
        return self.root_dist[u] + self.root_dist[v] - 2 * self.root_dist[a]

    def get_root_distance(self, v: int) -> int:
        """root-v パスの辺重みの総和を返す。"""
        self._ensure_built()
        return self.root_dist[v]

    def get_subtree_node_cost(self, v: int) -> int:
        """v の部分木に含まれる頂点コストの総和を返す。"""
        self._ensure_built()
        return self._subtree_node_cost[v]

    def get_subtree_edge_cost(self, v: int) -> int:
        """v の部分木内部に含まれる辺重みの総和を返す。"""
        self._ensure_built()
        return self._subtree_edge_cost[v]

    def get_root_node_cost(self, v: int) -> int:
        """root-v パスに含まれる頂点コストの総和を返す。"""
        self._ensure_built()
        return self._root_node_cost[v]

    def get_path_node_cost(self, u: int, v: int) -> int:
        """u-v パスに含まれる頂点コストの総和を返す。"""
        self._ensure_built()
        a = self.get_lca(u, v)
        return (
            self._root_node_cost[u]
            + self._root_node_cost[v]
            - 2 * self._root_node_cost[a]
            + self.node_cost[a]
        )

    # 旧 tree.py で使っていた名前との互換用
    def subtree_cost_node(self, v: int) -> int:
        return self.get_subtree_node_cost(v)

    def subtree_cost_edge(self, v: int) -> int:
        return self.get_subtree_edge_cost(v)

    def root_node_cost(self, v: int) -> int:
        return self.get_root_node_cost(v)

    def root_edge_cost(self, v: int) -> int:
        return self.get_root_distance(v)

    def dist_two_node_node(self, u: int, v: int) -> int:
        return self.get_path_node_cost(u, v)

    def dist_two_node_edge(self, u: int, v: int) -> int:
        return self.get_distance(u, v)
