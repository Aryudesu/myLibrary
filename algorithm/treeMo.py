from math import isqrt
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


class TreeMo(Generic[T]):
    """
    木上のパスクエリを Mo's Algorithm で処理する。

    各頂点を Euler Tour の行きがけ・帰りがけに 1 回ずつ記録し、
    現在区間に奇数回現れる頂点を active として管理する。

    クエリ (s, t) に対して、
        Odd(E[tin[s] + 1 : tin[t] + 1])
    に LCA(s, t) を一時的に加えることで s-t パスを表現する。
    ただし tin[s] <= tin[t] となるよう内部で入れ替える。

    頂点番号は 0-indexed。

    計算量:
        前処理 O(N log N)
        add/remove が O(F) のとき、
        おおむね O(N sqrt(Q) * F + Q log N)

    使用方法:
        mo = TreeMo(graph)
        qid = mo.addQuery(s, t)

        answers = mo.solve(
            addVertex,
            removeVertex,
            getAnswer,
        )

    getAnswer(queryIndex) にはクエリ番号が渡されるため、
    クエリ固有の追加パラメータは外部配列に保存して利用できる。
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
        self.up: list[list[int]] = [self.parent[:]]
        self.up[0][root] = root

        for _ in range(1, self.LOG):
            prev = self.up[-1]
            self.up.append([prev[prev[v]] for v in range(self.N)])

        # (l, r, lca, queryIndex)
        self.queries: list[tuple[int, int, int, int]] = []

    def _buildEulerTour(self) -> None:
        """
        各頂点を行きがけ・帰りがけに 1 回ずつ記録する。
        再帰を使わず、長さ 2N の Euler Tour を構築する。
        """
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
        s-t パスに対するクエリを追加する。

        Returns:
            クエリ番号。
        """
        assert 0 <= s < self.N
        assert 0 <= t < self.N

        if self.tin[s] > self.tin[t]:
            s, t = t, s

        w = self.lca(s, t)
        l = self.tin[s] + 1
        r = self.tin[t] + 1

        idx = len(self.queries)
        self.queries.append((l, r, w, idx))
        return idx

    def solve(
        self,
        addVertex: Callable[[int], None],
        removeVertex: Callable[[int], None],
        getAnswer: Callable[[int], T],
    ) -> list[T]:
        """
        登録済みクエリを木上 Mo で処理する。

        Args:
            addVertex(v):
                頂点 v が現在のパス集合に入るとき呼ばれる。

            removeVertex(v):
                頂点 v が現在のパス集合から外れるとき呼ばれる。

            getAnswer(queryIndex):
                現在のパスに対する答えを返す。
                queryIndex は addQuery の追加順。

        Returns:
            クエリ追加順の答え。
        """
        Q = len(self.queries)

        if Q == 0:
            return []

        M = len(self.euler)
        blockSize = max(1, M // max(1, isqrt(Q)))

        queries = sorted(
            self.queries,
            key=lambda q: (
                q[0] // blockSize,
                q[1]
                if (q[0] // blockSize) % 2 == 0
                else -q[1],
            ),
        )

        answers: list[T | None] = [None] * Q
        active = [False] * self.N

        def togglePosition(pos: int) -> None:
            v = self.euler[pos]

            if active[v]:
                removeVertex(v)
            else:
                addVertex(v)

            active[v] = not active[v]

        L = 0
        R = 0

        for l, r, w, idx in queries:
            while L > l:
                L -= 1
                togglePosition(L)

            while R < r:
                togglePosition(R)
                R += 1

            while L < l:
                togglePosition(L)
                L += 1

            while R > r:
                R -= 1
                togglePosition(R)

            # 上の Euler 区間には LCA は含まれない。
            # 回答時だけ一時的に追加する。
            addVertex(w)
            answers[idx] = getAnswer(idx)
            removeVertex(w)

        return answers  # type: ignore
