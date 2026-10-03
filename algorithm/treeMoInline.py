from math import sqrt


class TreeMoInline:
    """
    木上 Mo の前処理とクエリ順序付けだけを行う軽量クラス。

    通常の TreeMo のように add/remove/getAnswer をコールバックで呼ばず、
    solve のホットループを問題側へ直接書きたい場合に使う。

    目的:
        - Python で関数呼び出し回数を減らしたい
        - active / cnt / answer などをローカル変数へ落としたい
        - Mo の while ループ自体を問題固有に最適化したい

    頂点番号は 0-indexed。
    graph は無向木の隣接リストを想定する。
    各辺 (u, v) は graph[u], graph[v] の両方に追加する。

    使い方:
        tm = TreeMoInline(graph)

        for s, t in queries:
            tm.addQuery(s, t)

        ordered = tm.getOrderedQueries()

        E = tm.euler
        active = [False] * N
        L = R = 0

        for l, r, w, qi in ordered:
            while L > l:
                L -= 1
                v = E[L]
                # toggle をここへ直書き

            while R < r:
                v = E[R]
                R += 1
                # toggle をここへ直書き

            while L < l:
                v = E[L]
                L += 1
                # toggle をここへ直書き

            while R > r:
                R -= 1
                v = E[R]
                # toggle をここへ直書き

            # LCA w を一時的に add
            # answer[qi] = ...
            # LCA w を remove

    各クエリは (l, r, lca, queryIndex) に変換される。
    Euler Tour 上では半開区間 [l, r) を用いる。
    """

    def __init__(self, graph: list[list[int]], root: int = 0):
        self.graph = graph
        self.N = len(graph)

        assert self.N > 0
        assert 0 <= root < self.N

        self.root = root
        self.euler: list[int] = []
        self.tin = [-1] * self.N
        self.tout = [-1] * self.N
        self.parent = [-1] * self.N
        self.depth = [0] * self.N

        self._buildEulerTour()

        assert all(x != -1 for x in self.tin), "graph must be a connected tree"

        self.LOG = max(1, self.N.bit_length())
        self.up = [self.parent[:]]
        self.up[0][root] = root

        for _ in range(1, self.LOG):
            prev = self.up[-1]
            self.up.append([prev[prev[v]] for v in range(self.N)])

        self.queries: list[tuple[int, int, int, int]] = []

    def _buildEulerTour(self) -> None:
        """各頂点を行きがけ・帰りがけに1回ずつ記録する長さ2NのEuler Tour。"""
        stack = [(self.root, -1, 0)]

        while stack:
            v, p, state = stack.pop()

            if state == 0:
                self.parent[v] = v if p == -1 else p

                if p != -1:
                    self.depth[v] = self.depth[p] + 1

                self.tin[v] = len(self.euler)
                self.euler.append(v)

                stack.append((v, p, 1))

                for to in reversed(self.graph[v]):
                    if to == p:
                        continue
                    stack.append((to, v, 0))

            else:
                self.tout[v] = len(self.euler)
                self.euler.append(v)

    def lca(self, u: int, v: int) -> int:
        """u, v の LCA を返す。"""
        assert 0 <= u < self.N
        assert 0 <= v < self.N

        if self.depth[u] < self.depth[v]:
            u, v = v, u

        diff = self.depth[u] - self.depth[v]
        bit = 0

        while diff:
            if diff & 1:
                u = self.up[bit][u]
            diff >>= 1
            bit += 1

        if u == v:
            return u

        for k in range(self.LOG - 1, -1, -1):
            if self.up[k][u] != self.up[k][v]:
                u = self.up[k][u]
                v = self.up[k][v]

        return self.parent[u]

    def addQuery(self, s: int, t: int) -> int:
        """
        s-t パスのクエリを追加する。

        Returns:
            クエリ番号。
        """
        assert 0 <= s < self.N
        assert 0 <= t < self.N

        if self.tin[s] > self.tin[t]:
            s, t = t, s

        w = self.lca(s, t)

        # Odd(E[tin[s]+1 : tin[t]+1]) + LCA
        l = self.tin[s] + 1
        r = self.tin[t] + 1

        qi = len(self.queries)
        self.queries.append((l, r, w, qi))
        return qi

    def getBlockSize(self) -> int:
        """
        Mo の推奨ブロック幅を返す。

        木上 Mo の Euler Tour 長 M=2N に対し、
        M / sqrt(2Q/3) を目安にする。
        """
        Q = len(self.queries)

        if Q == 0:
            return 1

        M = len(self.euler)
        return max(1, int(M / sqrt(2.0 * Q / 3.0)))

    def getOrderedQueries(
        self,
        blockSize: int | None = None,
    ) -> list[tuple[int, int, int, int]]:
        """
        Mo 順に並べたクエリを返す。

        Returns:
            [(l, r, lca, queryIndex), ...]

        blockSize を省略した場合は getBlockSize() の値を利用する。
        """
        if blockSize is None:
            blockSize = self.getBlockSize()

        assert blockSize >= 1

        return sorted(
            self.queries,
            key=lambda q: (
                q[0] // blockSize,
                q[1]
                if (q[0] // blockSize) & 1
                else -q[1],
            ),
        )

    def __len__(self) -> int:
        return len(self.queries)
