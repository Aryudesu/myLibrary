from bisect import bisect_left, bisect_right
from typing import List, Optional


class BisectMapper:
    """bisectを個人的にわかりやすいようにしたかったやつ"""

    def __init__(self, A: Optional[List[int]] = None, sort: bool = True):
        """初期化"""
        A = A or []
        self.set_data(A, sort=sort)

    def set_data(self, A: List[int], sort: bool = True):
        """データをセットし直します"""
        self.data = sorted(A) if sort else A
        self.N = len(self.data)

    def leq_index(self, x: int) -> int:
        """
        x以下のデータの最大のインデックスを取得します．
        xがデータ内の最小値より小さければ-1を返却します．
        """
        i = bisect_right(self.data, x) - 1
        return i if 0 <= i < self.N else -1

    def lt_index(self, x: int) -> int:
        """
        x未満のデータの最大のインデックスを取得します．
        xがデータ内の最大値より大きければN，小さければ-1を返却します．
        """
        i = bisect_left(self.data, x) - 1
        return i if 0 <= i < self.N else -1

    def geq_index(self, x: int) -> int:
        """
        x以上のデータの最小のインデックスを取得します
        xがデータ内の最大値より大きければNを返却します．
        """
        i = bisect_left(self.data, x)
        return i

    def gt_index(self, x: int) -> int:
        """
        x超過のデータの最小のインデックスを取得します
        xがデータ内の最大値より大きければN，小さければ0を返却します．
        """
        i = bisect_right(self.data, x)
        return i

    def count_range(
        self,
        left: int,
        right: int,
        left_inclusive: bool = True,
        right_inclusive: bool = True,
    ) -> int:
        """
        範囲内の要素数を返します
        [left, right], [left, right), (left, right], (left, right)
        """
        if self.N == 0:
            return 0

        l = self.geq_index(left) if left_inclusive else self.gt_index(left)
        r = self.leq_index(right) if right_inclusive else self.lt_index(right)

        if l > r:
            return 0
        return r - l + 1


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
    bm.set_data(indices, sort=False)  # 既にソート済
    count = bm.count_range(L - 1, R - 1)
    print(count)
