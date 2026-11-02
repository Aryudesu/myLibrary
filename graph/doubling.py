"""
汎用ダブリング (0-indexed).

Doubling:
    関数グラフ上を指定回数ジャンプする。
DoublingMonoid:
    ジャンプ中に通過する頂点の値をモノイドで集約する。
    始点を含み、終点を含まない [v, nxt(v), ..., nxt^(steps-1)(v)] を集約する。

いずれも前計算 O(N log max_steps)、クエリ O(log max_steps)。
"""

from typing import Callable, TypeVar

T = TypeVar("T")


class Doubling:
    """各頂点から遷移先が1つに決まるグラフのダブリング。"""

    def __init__(self, to: list[int], max_steps: int = 10**18):
        if not to:
            raise ValueError("to must be non-empty")
        if max_steps < 0:
            raise ValueError("max_steps must be nonnegative")
        n = len(to)
        if any(v < 0 or v >= n for v in to):
            raise ValueError("invalid next vertex")
        self.n = n
        self.max_steps = max_steps
        self.log = max(1, max_steps.bit_length())
        self.nxt = [list(to)]
        for _ in range(1, self.log):
            prev = self.nxt[-1]
            self.nxt.append([prev[prev[v]] for v in range(n)])

    def jump(self, v: int, steps: int) -> int:
        """v から steps 回遷移した頂点を返す。O(log steps)。"""
        if not 0 <= v < self.n:
            raise IndexError("invalid start vertex")
        if not 0 <= steps <= self.max_steps:
            raise ValueError("steps out of precomputed range")
        bit = 0
        while steps:
            if steps & 1:
                v = self.nxt[bit][v]
            steps >>= 1
            bit += 1
        return v


class DoublingMonoid(Doubling):
    """
    経路上の頂点値をモノイドで集約するダブリング。

    values[v] は頂点 v に置く値。edge values を扱う場合は各辺 v->to[v]
    の値として values[v] を渡せばよい。
    op は結合的、identity は左右の単位元である必要がある。
    非可換な op も使用可能。
    """

    def __init__(
        self,
        to: list[int],
        values: list[T],
        op: Callable[[T, T], T],
        identity: T,
        max_steps: int = 10**18,
    ):
        if len(to) != len(values):
            raise ValueError("to and values must have the same length")
        super().__init__(to, max_steps)
        self.op = op
        self.identity = identity
        self.val = [list(values)]
        for k in range(1, self.log):
            prev = self.val[-1]
            mids = self.nxt[k - 1]
            self.val.append([
                op(prev[v], prev[mids[v]]) for v in range(self.n)
            ])

    def fold(self, v: int, steps: int) -> tuple[T, int]:
        """steps 個の頂点値を順に集約し、(集約値, 移動後の頂点)を返す。"""
        if not 0 <= v < self.n:
            raise IndexError("invalid start vertex")
        if not 0 <= steps <= self.max_steps:
            raise ValueError("steps out of precomputed range")
        result = self.identity
        bit = 0
        while steps:
            if steps & 1:
                result = self.op(result, self.val[bit][v])
                v = self.nxt[bit][v]
            steps >>= 1
            bit += 1
        return result, v

    def max_steps_while(
        self, v: int, predicate: Callable[[T], bool], limit: int
    ) -> tuple[int, int, T]:
        """
        集約値が predicate を満たす最大の移動数を求める。
        戻り値は (移動数, 移動後の頂点, 集約値)。

        predicate(identity) は True で、集約区間を右に伸ばすと
        True -> False にしか変化しない単調性が必要。
        limit 個まで調べる。閉路での無限ループ回避には limit=n が便利。
        """
        if not 0 <= v < self.n:
            raise IndexError("invalid start vertex")
        if not 0 <= limit <= self.max_steps:
            raise ValueError("limit out of precomputed range")
        if not predicate(self.identity):
            raise ValueError("predicate(identity) must be True")
        used = 0
        result = self.identity
        for k in range(self.log - 1, -1, -1):
            step = 1 << k
            if used + step > limit:
                continue
            candidate = self.op(result, self.val[k][v])
            if predicate(candidate):
                result = candidate
                v = self.nxt[k][v]
                used += step
        return used, v, result


if __name__ == "__main__":
    # AWC0191 E: 最初に学力が難易度以上になる生徒を探す
    # P = [1, 2, 3, 1]  # 0-indexed
    # S = [3, 5, 2, 10]
    # D = [2, 6, 9, 1]
    # db = DoublingMonoid(P, S, max, -1, max_steps=len(P))
    # ans = []
    # for i, difficulty in enumerate(D):
    #     skipped, v, _ = db.max_steps_while(
    #         i, lambda x, d=difficulty: x < d, len(P)
    #     )
    #     ans.append(v + 1 if skipped < len(P) else -1)
    # assert ans == [1, 4, 4, 4]

    db = Doubling([1, 2, 0], max_steps=100)
    assert db.jump(0, 0) == 0
    assert db.jump(0, 5) == 2
    dm = DoublingMonoid([1, 2, 0], [2, 3, 5], max, -1, 100)
    assert dm.fold(0, 4) == (5, 1)
    assert dm.max_steps_while(0, lambda x: x < 5, 3)[:2] == (2, 2)
