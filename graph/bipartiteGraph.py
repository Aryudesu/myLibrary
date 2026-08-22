from collections import deque
from typing import Iterable
# keywords:
# bipartite
# 2-coloring
# odd cycle
# 奇閉路
# 奇数閉路
# 非二部グラフ

class BipartiteGraph:
    """
    無向グラフの二部グラフ判定・二部彩色クラス（0-indexed）

    主な機能:
        - 二部グラフか判定
        - 各頂点を 0 / 1 に彩色
        - 連結成分IDを取得
        - 各連結成分について色ごとの頂点集合を取得
        - 二部グラフでない場合、奇閉路を1つ復元
        - 各連結成分が二部グラフか判定

    使用方法:
        bg = BipartiteGraph(n)

        for u, v in edges:
            bg.add_edge(u, v)

        if bg.build():
            print(bg.color)
        else:
            print(bg.odd_cycle)

    計算量:
        構築: O(N + M)
        メモリ: O(N + M)
    """

    def __init__(
        self,
        n: int,
        edges: Iterable[tuple[int, int]] | None = None,
    ):
        if n < 0:
            raise ValueError("頂点数は0以上である必要があります")

        self.n = n
        self.graph = [[] for _ in range(n)]

        if edges is not None:
            for u, v in edges:
                self.add_edge(u, v)

        self._built = False

        # build() 後に設定される
        self.is_bipartite = True
        self.color = [-1] * n
        self.component_id = [-1] * n
        self.parent = [-1] * n
        self.depth = [-1] * n

        # groups[cid] = (色0の頂点列, 色1の頂点列)
        self.groups: list[tuple[list[int], list[int]]] = []

        # 各連結成分が二部グラフか
        self.component_is_bipartite: list[bool] = []

        # 二部グラフでない場合の奇閉路
        #
        # 頂点列 [v0, v1, ..., vk] として、
        # vi - v(i+1) および vk - v0 に辺がある。
        #
        # 自己ループの場合は [v]。
        self.odd_cycle: list[int] | None = None

    def _validate_vertex(self, v: int) -> None:
        if not 0 <= v < self.n:
            raise IndexError(
                f"頂点は 0 以上 {self.n} 未満である必要があります"
            )

    def add_edge(self, u: int, v: int) -> None:
        """
        無向辺 u - v を追加する。

        自己ループ・多重辺も追加可能。
        自己ループが存在するグラフは二部グラフではない。
        """

        self._validate_vertex(u)
        self._validate_vertex(v)

        self.graph[u].append(v)
        self.graph[v].append(u)

        self._built = False

    def build(self) -> bool:
        """
        二部グラフ判定と彩色を行う。

        戻り値:
            グラフ全体が二部グラフなら True
            そうでなければ False

        計算量:
            O(N + M)
        """

        self.is_bipartite = True
        self.color = [-1] * self.n
        self.component_id = [-1] * self.n
        self.parent = [-1] * self.n
        self.depth = [-1] * self.n

        self.groups = []
        self.component_is_bipartite = []
        self.odd_cycle = None

        for start in range(self.n):
            if self.color[start] != -1:
                continue

            cid = len(self.groups)

            side_zero: list[int] = []
            side_one: list[int] = []

            component_ok = True

            self.color[start] = 0
            self.component_id[start] = cid
            self.depth[start] = 0

            queue = deque([start])

            while queue:
                v = queue.popleft()

                if self.color[v] == 0:
                    side_zero.append(v)
                else:
                    side_one.append(v)

                for nv in self.graph[v]:
                    if self.color[nv] == -1:
                        self.color[nv] = self.color[v] ^ 1
                        self.component_id[nv] = cid
                        self.parent[nv] = v
                        self.depth[nv] = self.depth[v] + 1

                        queue.append(nv)

                    elif self.color[nv] == self.color[v]:
                        component_ok = False
                        self.is_bipartite = False

                        if self.odd_cycle is None:
                            self.odd_cycle = (
                                self._restore_odd_cycle(v, nv)
                            )

            self.groups.append((side_zero, side_one))
            self.component_is_bipartite.append(component_ok)

        self._built = True
        return self.is_bipartite

    def _restore_odd_cycle(self, u: int, v: int) -> list[int]:
        """
        同じ色で結ばれた辺 u - v と BFS 木から奇閉路を復元する。

        戻り値の最後と最初の間にも辺があるものとする。
        """

        # 自己ループ
        if u == v:
            return [u]

        path_u: list[int] = []
        path_v: list[int] = []

        x = u
        y = v

        while self.depth[x] > self.depth[y]:
            path_u.append(x)
            x = self.parent[x]

        while self.depth[y] > self.depth[x]:
            path_v.append(y)
            y = self.parent[y]

        while x != y:
            path_u.append(x)
            path_v.append(y)

            x = self.parent[x]
            y = self.parent[y]

        # LCA
        path_u.append(x)

        # u -> ... -> LCA -> ... -> v
        # 最後に競合辺 v -> u で閉じる
        return path_u + path_v[::-1]

    def _require_built(self) -> None:
        if not self._built:
            raise RuntimeError(
                "先に build() を実行してください"
            )

    @property
    def component_count(self) -> int:
        """連結成分数を返す。"""

        self._require_built()
        return len(self.groups)

    def get_group(
        self,
        component_id: int,
    ) -> tuple[list[int], list[int]]:
        """
        指定した連結成分の色0・色1の頂点集合を返す。

        内部配列のコピーを返す。
        """

        self._require_built()

        if not 0 <= component_id < self.component_count:
            raise IndexError(
                "連結成分IDが範囲外です"
            )

        side_zero, side_one = self.groups[component_id]

        return side_zero[:], side_one[:]

    def get_component_vertices(self, v: int) -> list[int]:
        """
        頂点 v と同じ連結成分に属する頂点列を返す。
        """

        self._require_built()
        self._validate_vertex(v)

        side_zero, side_one = self.groups[
            self.component_id[v]
        ]

        return side_zero + side_one

    def get_side_vertices(self, v: int) -> list[int]:
        """
        頂点 v と同じ連結成分かつ、同じ色の頂点列を返す。

        対象成分が二部グラフでない場合、
        この彩色は正しい二部彩色ではない点に注意。
        """

        self._require_built()
        self._validate_vertex(v)

        return self.groups[
            self.component_id[v]
        ][self.color[v]][:]

    def same_component(self, u: int, v: int) -> bool:
        """
        u と v が同じ連結成分に属するかを返す。
        """

        self._require_built()
        self._validate_vertex(u)
        self._validate_vertex(v)

        return (
            self.component_id[u]
            == self.component_id[v]
        )

    def same_color(self, u: int, v: int) -> bool:
        """
        u と v が同じ連結成分で、同じ色かを返す。

        異なる連結成分の場合は False。

        対象成分が二部グラフでない場合、
        色の意味は二部グラフとして保証されない。
        """

        self._require_built()
        self._validate_vertex(u)
        self._validate_vertex(v)

        return (
            self.component_id[u]
            == self.component_id[v]
            and self.color[u] == self.color[v]
        )

    def opposite_color(self, u: int, v: int) -> bool:
        """
        u と v が同じ連結成分で、異なる色かを返す。

        異なる連結成分の場合は False。
        """

        self._require_built()
        self._validate_vertex(u)
        self._validate_vertex(v)

        return (
            self.component_id[u]
            == self.component_id[v]
            and self.color[u] != self.color[v]
        )

    def color_counts(self, component_id: int) -> tuple[int, int]:
        """
        指定した連結成分について、
        色0・色1の頂点数を返す。
        """

        self._require_built()

        if not 0 <= component_id < self.component_count:
            raise IndexError(
                "連結成分IDが範囲外です"
            )

        side_zero, side_one = self.groups[component_id]

        return len(side_zero), len(side_one)

