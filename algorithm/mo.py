from typing import Callable, TypeVar, Generic
from math import isqrt

T = TypeVar("T")


class Mo(Generic[T]):
    """
    Mo's Algorithm

    静的配列に対するオフライン区間クエリを処理する。

    適用条件:
        - クエリの処理順を並べ替えてよい
        - 配列の更新がない
        - 現在区間 [L, R) に対する要素の追加・削除を高速に処理できる

    計算量:
        add/remove が O(F) のとき、
        おおむね O((N + Q) * sqrt(N) * F)

    区間はすべて半開区間 [l, r) とする。
    """

    def __init__(self, N: int):
        self.N = N
        self.queries: list[tuple[int, int, int]] = []

    def addQuery(self, l: int, r: int) -> int:
        """
        区間クエリ [l, r) を追加する。

        Returns:
            クエリ番号
        """
        assert 0 <= l <= r <= self.N

        idx = len(self.queries)
        self.queries.append((l, r, idx))
        return idx

    def solve(
        self,
        add: Callable[[int], None],
        remove: Callable[[int], None],
        getAnswer: Callable[[], T],
    ) -> list[T]:
        """
        Mo's Algorithmで全クエリを処理する。

        Args:
            add(i):
                index i の要素を現在区間へ追加する。

            remove(i):
                index i の要素を現在区間から削除する。

            getAnswer():
                現在区間に対する答えを返す。

        Returns:
            クエリ追加順の答え。
        """
        Q = len(self.queries)

        if Q == 0:
            return []

        # N / sqrt(Q) 程度にすると、
        # N と Q の大きさが異なる場合にも比較的安定する。
        blockSize = max(1, self.N // max(1, isqrt(Q)))

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

        L = 0
        R = 0

        for l, r, idx in queries:

            while L > l:
                L -= 1
                add(L)

            while R < r:
                add(R)
                R += 1

            while L < l:
                remove(L)
                L += 1

            while R > r:
                R -= 1
                remove(R)

            answers[idx] = getAnswer()

        return answers  # type: ignore