from collections import deque
from typing import Iterable


class FunctionalGraph:
    """
    Functional Graph 用クラス（0-indexed）

    各頂点 v から、ちょうど1本の有向辺 v -> to[v] が伸びるグラフを扱います。

    主な機能:
        - サイクル分解
        - 各頂点からサイクルまでの距離
        - 各頂点が最初に到達するサイクル頂点
        - k 回遷移した先の頂点
        - u から v に到達可能か、および最短遷移回数
        - 同じ連結成分に属するか
        - 各サイクルの頂点列

    計算量:
        構築:
            O(N log N)

        jump(v, k):
            O(log N)

        distance(u, v):
            O(log N)

        その他の参照:
            O(1)

    メモリ:
        O(N log N)
    """

    def __init__(self, to: Iterable[int]):
        self.to = list(to)
        self.n = len(self.to)

        if self.n == 0:
            raise ValueError("頂点数は1以上である必要があります")

        for v in self.to:
            if not 0 <= v < self.n:
                raise ValueError(
                    f"遷移先は 0 以上 {self.n} 未満である必要があります"
                )

        self.rev_graph = [[] for _ in range(self.n)]
        indegree = [0] * self.n

        for v, nv in enumerate(self.to):
            self.rev_graph[nv].append(v)
            indegree[nv] += 1

        # 葉側から削除し、最後に残った頂点をサイクル頂点とする
        queue = deque(
            v for v in range(self.n)
            if indegree[v] == 0
        )

        removed = [False] * self.n

        while queue:
            v = queue.popleft()
            removed[v] = True

            nv = self.to[v]
            indegree[nv] -= 1

            if indegree[nv] == 0:
                queue.append(nv)

        self.in_cycle = [
            not removed[v]
            for v in range(self.n)
        ]

        # cycle_id[v]:
        #   v が属する Functional Graph 成分のID
        #
        # Functional Graphの各弱連結成分には
        # ちょうど1個のサイクルがあるため、
        # cycle_id はそのまま連結成分IDとして使える
        self.cycle_id = [-1] * self.n

        # cycle_pos[v]:
        #   サイクル上での位置
        #   サイクル外なら -1
        self.cycle_pos = [-1] * self.n

        # depth[v]:
        #   v からサイクルまでの遷移回数
        #   サイクル上なら 0
        self.depth = [-1] * self.n

        # entry[v]:
        #   v から遷移し続けたとき、
        #   最初に到達するサイクル頂点
        self.entry = [-1] * self.n

        # cycles[cid]:
        #   サイクルを遷移順に並べた頂点列
        self.cycles: list[list[int]] = []

        self._build_cycles()
        self._build_tree_information()

        self.cycle_size = [
            len(cycle)
            for cycle in self.cycles
        ]

        self._build_doubling()

    def _build_cycles(self) -> None:
        """各サイクルを列挙する"""

        for start in range(self.n):
            if not self.in_cycle[start]:
                continue

            if self.cycle_id[start] != -1:
                continue

            cid = len(self.cycles)
            cycle = []

            v = start

            while True:
                self.cycle_id[v] = cid
                self.cycle_pos[v] = len(cycle)
                self.depth[v] = 0
                self.entry[v] = v

                cycle.append(v)

                v = self.to[v]

                if v == start:
                    break

            self.cycles.append(cycle)

    def _build_tree_information(self) -> None:
        """
        各サイクルから逆辺を辿り、
        サイクルへ流れ込む木部分の情報を計算する
        """

        queue = deque(
            v
            for cycle in self.cycles
            for v in cycle
        )

        while queue:
            v = queue.popleft()

            for prev in self.rev_graph[v]:
                if self.cycle_id[prev] != -1:
                    continue

                self.cycle_id[prev] = self.cycle_id[v]
                self.depth[prev] = self.depth[v] + 1
                self.entry[prev] = self.entry[v]

                queue.append(prev)

    def _build_doubling(self) -> None:
        """
        木部分を移動するためのDoublingテーブルを構築する。

        サイクル上を巨大回数移動する場合は
        cycle_pos と剰余を利用するため、
        log N 段だけあればよい。
        """

        self.log = max(1, self.n.bit_length())

        self.up = [self.to[:]]

        for _ in range(1, self.log):
            prev = self.up[-1]

            self.up.append([
                prev[prev[v]]
                for v in range(self.n)
            ])

    def _validate_vertex(self, v: int) -> None:
        if not 0 <= v < self.n:
            raise IndexError(
                f"頂点は 0 以上 {self.n} 未満である必要があります"
            )

    def _jump_small(self, v: int, k: int) -> int:
        """
        k < N 程度の遷移をDoublingで行う内部関数
        """

        bit = 0

        while k:
            if k & 1:
                v = self.up[bit][v]

            k >>= 1
            bit += 1

        return v

    def jump(self, v: int, k: int) -> int:
        """
        頂点 v から k 回遷移した先の頂点を返す。

        k は非常に大きい整数でもよい。

        計算量:
            O(log N)
        """

        self._validate_vertex(v)

        if k < 0:
            raise ValueError("k は非負整数である必要があります")

        distance_to_cycle = self.depth[v]

        # まだ木部分にいる
        if k < distance_to_cycle:
            return self._jump_small(v, k)

        # サイクルに到達した後は剰余で処理
        entry = self.entry[v]
        cid = self.cycle_id[v]
        cycle = self.cycles[cid]
        cycle_length = len(cycle)

        remaining = (
            k - distance_to_cycle
        ) % cycle_length

        position = self.cycle_pos[entry]

        return cycle[
            (position + remaining) % cycle_length
        ]

    def distance(self, u: int, v: int) -> int | None:
        """
        u から遷移を繰り返して v に到達する場合、
        最小遷移回数を返す。

        到達できない場合は None を返す。

        計算量:
            O(log N)
        """

        self._validate_vertex(u)
        self._validate_vertex(v)

        # 属するサイクルが異なるなら到達不能
        if self.cycle_id[u] != self.cycle_id[v]:
            return None

        # v が木部分にいる場合、
        # u も同じ枝の上流にいる必要がある
        if self.depth[v] > 0:
            diff = self.depth[u] - self.depth[v]

            if diff < 0:
                return None

            if self._jump_small(u, diff) == v:
                return diff

            return None

        # v がサイクル上の場合
        cid = self.cycle_id[u]
        cycle_length = self.cycle_size[cid]

        entry = self.entry[u]

        cycle_distance = (
            self.cycle_pos[v]
            - self.cycle_pos[entry]
        ) % cycle_length

        return self.depth[u] + cycle_distance

    def reachable(self, u: int, v: int) -> bool:
        """
        u から v に到達可能かを返す。

        計算量:
            O(log N)
        """

        return self.distance(u, v) is not None

    def same_component(self, u: int, v: int) -> bool:
        """
        u と v が同じ弱連結成分に属するかを返す。

        Functional Graphでは、
        同じサイクルへ流れ込む頂点同士が同じ成分となる。

        計算量:
            O(1)
        """

        self._validate_vertex(u)
        self._validate_vertex(v)

        return self.cycle_id[u] == self.cycle_id[v]

    def get_cycle(self, v: int) -> list[int]:
        """
        v が属する成分のサイクルを遷移順で返す。

        返り値は内部配列のコピー。

        計算量:
            O(サイクル長)
        """

        self._validate_vertex(v)

        return self.cycles[
            self.cycle_id[v]
        ][:]

    def get_cycle_length(self, v: int) -> int:
        """
        v が属する成分のサイクル長を返す。

        計算量:
            O(1)
        """

        self._validate_vertex(v)

        return self.cycle_size[
            self.cycle_id[v]
        ]

    def distinct_orbit_size(self, v: int) -> int:
        """
        v から遷移を繰り返したときに登場する
        異なる頂点の個数を返す。

        サイクルまでの距離 + サイクル長。

        計算量:
            O(1)
        """

        self._validate_vertex(v)

        return (
            self.depth[v]
            + self.cycle_size[self.cycle_id[v]]
        )