from collections import deque
from typing import Iterable


class FunctionalGraph:
    """
    Functional Graph 用クラス（0-indexed）。

    各頂点 v からちょうど1本の有向辺 v -> to[v] が伸びるグラフを扱う。

    主な機能:
    - サイクル分解
    - 各頂点からサイクルまでの距離
    - 各頂点が最初に到達するサイクル頂点
    - k 回遷移した先の頂点
    - u から v への到達可能性 / 最短遷移回数
    - 弱連結成分判定
    - サイクル列挙
    - 始点から最初の再訪までの軌道取得

    構築 O(N log N)、jump / distance O(log N)、その他多くは O(1)。
    """

    def __init__(self, to: Iterable[int]):
        self.to = list(to)
        self.n = len(self.to)

        if self.n == 0:
            raise ValueError("頂点数は1以上である必要があります")

        for v in self.to:
            if not 0 <= v < self.n:
                raise ValueError(f"遷移先は 0 以上 {self.n} 未満である必要があります")

        self.rev_graph = [[] for _ in range(self.n)]
        indegree = [0] * self.n

        for v, nv in enumerate(self.to):
            self.rev_graph[nv].append(v)
            indegree[nv] += 1

        queue = deque(v for v in range(self.n) if indegree[v] == 0)
        removed = [False] * self.n

        while queue:
            v = queue.popleft()
            removed[v] = True
            nv = self.to[v]
            indegree[nv] -= 1
            if indegree[nv] == 0:
                queue.append(nv)

        self.in_cycle = [not removed[v] for v in range(self.n)]
        self.cycle_id = [-1] * self.n
        self.cycle_pos = [-1] * self.n
        self.depth = [-1] * self.n
        self.entry = [-1] * self.n
        self.cycles: list[list[int]] = []

        self._build_cycles()
        self._build_tree_information()

        self.cycle_size = [len(cycle) for cycle in self.cycles]
        self._build_doubling()

    def _build_cycles(self) -> None:
        for start in range(self.n):
            if not self.in_cycle[start] or self.cycle_id[start] != -1:
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
        queue = deque(v for cycle in self.cycles for v in cycle)

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
        self.log = max(1, self.n.bit_length())
        self.up = [self.to[:]]
        for _ in range(1, self.log):
            prev = self.up[-1]
            self.up.append([prev[prev[v]] for v in range(self.n)])

    def _validate_vertex(self, v: int) -> None:
        if not 0 <= v < self.n:
            raise IndexError(f"頂点は 0 以上 {self.n} 未満である必要があります")

    def _jump_small(self, v: int, k: int) -> int:
        bit = 0
        while k:
            if k & 1:
                v = self.up[bit][v]
            k >>= 1
            bit += 1
        return v

    def jump(self, v: int, k: int) -> int:
        """頂点 v から k 回遷移した先を返す。k は巨大整数でもよい。"""
        self._validate_vertex(v)
        if k < 0:
            raise ValueError("k は非負整数である必要があります")

        distance_to_cycle = self.depth[v]
        if k < distance_to_cycle:
            return self._jump_small(v, k)

        entry = self.entry[v]
        cid = self.cycle_id[v]
        cycle = self.cycles[cid]
        remaining = (k - distance_to_cycle) % len(cycle)
        position = self.cycle_pos[entry]
        return cycle[(position + remaining) % len(cycle)]

    def kth(self, start: int, k: int) -> int:
        """旧 functional.py の kth 相当。start から k 回遷移した先を返す。"""
        return self.jump(start, k)

    def distance(self, u: int, v: int) -> int | None:
        """u から v に到達する最小遷移回数。到達不能なら None。"""
        self._validate_vertex(u)
        self._validate_vertex(v)

        if self.cycle_id[u] != self.cycle_id[v]:
            return None

        if self.depth[v] > 0:
            diff = self.depth[u] - self.depth[v]
            if diff < 0:
                return None
            return diff if self._jump_small(u, diff) == v else None

        cid = self.cycle_id[u]
        cycle_length = self.cycle_size[cid]
        entry = self.entry[u]
        cycle_distance = (self.cycle_pos[v] - self.cycle_pos[entry]) % cycle_length
        return self.depth[u] + cycle_distance

    def reachable(self, u: int, v: int) -> bool:
        return self.distance(u, v) is not None

    def same_component(self, u: int, v: int) -> bool:
        self._validate_vertex(u)
        self._validate_vertex(v)
        return self.cycle_id[u] == self.cycle_id[v]

    def get_cycle(self, v: int) -> list[int]:
        self._validate_vertex(v)
        return self.cycles[self.cycle_id[v]][:]

    def get_cycle_length(self, v: int) -> int:
        self._validate_vertex(v)
        return self.cycle_size[self.cycle_id[v]]

    def distinct_orbit_size(self, v: int) -> int:
        """v から最初に頂点が再訪されるまでに現れる異なる頂点数。"""
        self._validate_vertex(v)
        return self.depth[v] + self.cycle_size[self.cycle_id[v]]

    def orbit(self, start: int) -> list[int]:
        """start から最初に頂点が再訪される直前までの頂点列を返す。"""
        self._validate_vertex(start)
        prefix_len = self.depth[start]
        cycle = self.cycles[self.cycle_id[start]]
        result = []
        v = start
        for _ in range(prefix_len):
            result.append(v)
            v = self.to[v]

        entry_pos = self.cycle_pos[v]
        result.extend(cycle[entry_pos:])
        result.extend(cycle[:entry_pos])
        return result

    def get_loop_start_index(self, start: int) -> int:
        """orbit(start) においてサイクル部分が始まる添字を返す。"""
        self._validate_vertex(start)
        return self.depth[start]

    def get_loop(self, start: int) -> list[int]:
        """start から到達するサイクルを、最初に到達する頂点から順に返す。"""
        self._validate_vertex(start)
        entry = self.entry[start]
        cycle = self.cycles[self.cycle_id[start]]
        pos = self.cycle_pos[entry]
        return cycle[pos:] + cycle[:pos]

    def is_in_loop(self, start: int, v: int) -> bool:
        """v が start から到達するサイクル部分に含まれるか。"""
        self._validate_vertex(start)
        self._validate_vertex(v)
        return self.cycle_id[start] == self.cycle_id[v] and self.in_cycle[v]
