import bisect
from collections.abc import Iterable
from typing import List, Optional


class BisectMapper:
    """
    bisect のマッパ
    self.data はソート済み前提
    """

    def __init__(self, data: Optional[Iterable[int]] = None, *, sort: bool = True) -> None:
        if data is None:
            self.data: List[int] = []
        else:
            self.data = list(data)
            if sort:
                self.data.sort()
        self.N = len(self.data)

    def _refresh_size(self) -> None:
        self.N = len(self.data)

    def set_data(self, data: Iterable[int], *, sort: bool = True) -> None:
        """データを入れ替える（必要ならソート）"""
        self.data = list(data)
        if sort:
            self.data.sort()
        self._refresh_size()

    # ------- インデックス -------

    def data_leq(self, x: int) -> int:
        """
        x 以下で最大の要素のインデックスを返す。
        該当要素がなければ -1。
        """
        i = bisect.bisect_right(self.data, x) - 1
        return i  # -1 ～ N-1

    def data_geq(self, x: int) -> int:
        """
        x 以上で最小の要素のインデックスを返す。
        該当要素がなければ N。
        """
        i = bisect.bisect_left(self.data, x)
        return i  # 0 ～ N

    def data_lt(self, x: int) -> int:
        """
        x 未満で最大の要素のインデックスを返す。
        該当要素がなければ -1。
        """
        i = bisect.bisect_left(self.data, x) - 1
        return i  # -1 ～ N-1

    def data_gt(self, x: int) -> int:
        """
        x 超過で最小の要素のインデックスを返す。
        該当要素がなければ N。
        """
        i = bisect.bisect_right(self.data, x)
        return i  # 0 ～ N

    data_l = data_lt
    data_g = data_gt

    # ------- 区間カウント -------

    def _count_between(self, a: int, b: int, left_closed: bool, right_closed: bool) -> int:
        """
        汎用: (left_closed ? [a : ) : (a : ) と、
              (right_closed ? : b] : : b) の間の要素数。
        """
        if a > b:
            return 0

        if left_closed:
            left = bisect.bisect_left(self.data, a)
        else:
            left = bisect.bisect_right(self.data, a)

        if right_closed:
            right = bisect.bisect_right(self.data, b)
        else:
            right = bisect.bisect_left(self.data, b)

        if right < left:
            return 0
        return right - left

    def between_c_c(self, a: int, b: int) -> int:
        """[a, b] に含まれる要素数"""
        return self._count_between(a, b, left_closed=True, right_closed=True)

    def between_c_o(self, a: int, b: int) -> int:
        """[a, b) に含まれる要素数"""
        return self._count_between(a, b, left_closed=True, right_closed=False)

    def between_o_c(self, a: int, b: int) -> int:
        """(a, b] に含まれる要素数"""
        return self._count_between(a, b, left_closed=False, right_closed=True)

    def between_o_o(self, a: int, b: int) -> int:
        """(a, b) に含まれる要素数"""
        return self._count_between(a, b, left_closed=False, right_closed=False)



# # *** Example (ABC248 D) ***
N = int(input())
A = [int(l) for l in input().split()]
Q = int(input())
position_map = {}
for i, val in enumerate(A):
    position_map.setdefault(val, []).append(i)

bm = BisectMapper()

for _ in range(Q):
    L, R, X = map(int, input().split())
    indices = position_map.get(X, [])
    if not indices:
        print(0)
        continue
    bm.set_data(indices, sort = False)
    count = bm.between_c_c(L - 1, R - 1)
    print(count)
