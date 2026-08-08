from bisect import bisect_left, bisect_right


class DynamicRangeOrderStatistics:
    """
    点更新 + 区間順序統計データ構造
    0-indexed / 半開区間 [l, r)

    構築時に、今後発生する更新 (index, value) をすべて渡す必要がある。
    いわゆる offline dynamic な構造。

    対応:
        set(i, x)

        range_sum(l, r)

        kth_smallest(l, r, k)
        kth_largest(l, r, k)

        count_less(l, r, x)
        count_le(l, r, x)

        sum_less(l, r, x)
        sum_le(l, r, x)

        sum_k_smallest(l, r, k)
        sum_k_largest(l, r, k)

        min_count_for_sum_ge(l, r, x)
            ※ 値が非負の場合を想定

    計算量:
        更新                  O(log V log N)
        kth                   O(log V log N)
        sum_k                 O(log V log N)
        min_count_for_sum_ge  O(log V log N)
        count/sum threshold   O(log V log N)

    V = 値の種類数
    """

    def __init__(
        self,
        a: list[int],
        updates: list[tuple[int, int]],
    ):
        self.n = len(a)
        self.a = a[:]

        # 各 index が将来取り得る値
        candidates = [[x] for x in a]

        values = set(a)

        for i, x in updates:
            candidates[i].append(x)
            values.add(x)

        self.values = sorted(values)
        self.m = len(self.values)

        self.value_id = {
            x: i
            for i, x in enumerate(self.values)
        }

        size = 1
        while size < self.m:
            size <<= 1

        self.size = size

        # 値Segment Treeの各ノードに
        # そのノードへ入り得る index を集める
        node_positions = [[] for _ in range(2 * size)]

        for i, xs in enumerate(candidates):
            for x in set(xs):
                node = size + self.value_id[x]

                while node:
                    node_positions[node].append(i)
                    node >>= 1

        self.positions = [None] * (2 * size)
        self.bit_count = [None] * (2 * size)
        self.bit_sum = [None] * (2 * size)

        for node in range(1, 2 * size):
            if not node_positions[node]:
                continue

            positions = sorted(set(node_positions[node]))

            self.positions[node] = positions

            m = len(positions)

            self.bit_count[node] = [0] * (m + 1)
            self.bit_sum[node] = [0] * (m + 1)

        # 初期値を登録
        for i, x in enumerate(a):
            self._add_value(i, x, 1)

    # =========================================================
    # Fenwick Tree
    # =========================================================

    @staticmethod
    def _bit_add(
        bit: list[int],
        i: int,
        x: int,
    ) -> None:

        n = len(bit)

        while i < n:
            bit[i] += x
            i += i & -i

    @staticmethod
    def _bit_sum(
        bit: list[int],
        i: int,
    ) -> int:

        res = 0

        while i:
            res += bit[i]
            i -= i & -i

        return res

    # =========================================================
    # internal query
    # =========================================================

    def _node_query(
        self,
        node: int,
        l: int,
        r: int,
    ) -> tuple[int, int]:
        """
        値Segment Tree上の node に属する値について、
        index in [l, r) の

            (個数, 総和)

        を返す。
        """

        positions = self.positions[node]

        if positions is None:
            return 0, 0

        li = bisect_left(positions, l)
        ri = bisect_left(positions, r)

        bit_count = self.bit_count[node]
        bit_sum = self.bit_sum[node]

        count = (
            self._bit_sum(bit_count, ri)
            - self._bit_sum(bit_count, li)
        )

        total = (
            self._bit_sum(bit_sum, ri)
            - self._bit_sum(bit_sum, li)
        )

        return count, total

    def _add_value(
        self,
        index: int,
        value: int,
        sign: int,
    ) -> None:

        node = self.size + self.value_id[value]

        while node:
            positions = self.positions[node]

            j = bisect_left(positions, index) + 1

            self._bit_add(
                self.bit_count[node],
                j,
                sign,
            )

            self._bit_add(
                self.bit_sum[node],
                j,
                sign * value,
            )

            node >>= 1

    def _prefix_value_query(
        self,
        l: int,
        r: int,
        end: int,
    ) -> tuple[int, int]:
        """
        圧縮後 value_id < end の値について、

            (個数, 総和)

        を返す。
        """

        left = self.size
        right = self.size + end

        count = 0
        total = 0

        while left < right:

            if left & 1:
                c, s = self._node_query(
                    left,
                    l,
                    r,
                )

                count += c
                total += s

                left += 1

            if right & 1:
                right -= 1

                c, s = self._node_query(
                    right,
                    l,
                    r,
                )

                count += c
                total += s

            left >>= 1
            right >>= 1

        return count, total

    # =========================================================
    # update
    # =========================================================

    def set(
        self,
        index: int,
        value: int,
    ) -> None:
        """
        a[index] = value
        """

        old = self.a[index]

        if old == value:
            return

        self._add_value(
            index,
            old,
            -1,
        )

        self._add_value(
            index,
            value,
            1,
        )

        self.a[index] = value

    # =========================================================
    # basic
    # =========================================================

    def range_sum(
        self,
        l: int,
        r: int,
    ) -> int:
        """
        sum(a[l:r])
        """

        return self._node_query(
            1,
            l,
            r,
        )[1]

    # =========================================================
    # kth
    # =========================================================

    def kth_smallest(
        self,
        l: int,
        r: int,
        k: int,
    ) -> int:
        """
        a[l:r] の k 番目に小さい値。
        k は 0-indexed。
        """

        if not 0 <= k < r - l:
            raise IndexError

        node = 1

        while node < self.size:

            left = node * 2

            count, _ = self._node_query(
                left,
                l,
                r,
            )

            if k < count:
                node = left

            else:
                k -= count
                node = left + 1

        return self.values[node - self.size]

    def kth_largest(
        self,
        l: int,
        r: int,
        k: int,
    ) -> int:
        """
        a[l:r] の k 番目に大きい値。
        k は 0-indexed。
        """

        return self.kth_smallest(
            l,
            r,
            r - l - 1 - k,
        )

    # =========================================================
    # threshold count
    # =========================================================

    def count_less(
        self,
        l: int,
        r: int,
        x: int,
    ) -> int:
        """
        a[l:r] で x 未満の要素数。
        """

        index = bisect_left(
            self.values,
            x,
        )

        return self._prefix_value_query(
            l,
            r,
            index,
        )[0]

    def count_le(
        self,
        l: int,
        r: int,
        x: int,
    ) -> int:
        """
        a[l:r] で x 以下の要素数。
        """

        index = bisect_right(
            self.values,
            x,
        )

        return self._prefix_value_query(
            l,
            r,
            index,
        )[0]

    # =========================================================
    # threshold sum
    # =========================================================

    def sum_less(
        self,
        l: int,
        r: int,
        x: int,
    ) -> int:
        """
        a[l:r] のうち x 未満の値の総和。
        """

        index = bisect_left(
            self.values,
            x,
        )

        return self._prefix_value_query(
            l,
            r,
            index,
        )[1]

    def sum_le(
        self,
        l: int,
        r: int,
        x: int,
    ) -> int:
        """
        a[l:r] のうち x 以下の値の総和。
        """

        index = bisect_right(
            self.values,
            x,
        )

        return self._prefix_value_query(
            l,
            r,
            index,
        )[1]

    # =========================================================
    # sum of k elements
    # =========================================================

    def sum_k_smallest(
        self,
        l: int,
        r: int,
        k: int,
    ) -> int:
        """
        a[l:r] の小さい方から k 個の総和。
        """

        if not 0 <= k <= r - l:
            raise ValueError

        if k == 0:
            return 0

        node = 1
        answer = 0

        while node < self.size:

            left = node * 2

            count, total = self._node_query(
                left,
                l,
                r,
            )

            if k <= count:
                node = left

            else:
                answer += total
                k -= count
                node = left + 1

        if k:
            value = self.values[node - self.size]
            answer += value * k

        return answer

    def sum_k_largest(
        self,
        l: int,
        r: int,
        k: int,
    ) -> int:
        """
        a[l:r] の大きい方から k 個の総和。
        """

        if not 0 <= k <= r - l:
            raise ValueError

        return (
            self.range_sum(l, r)
            - self.sum_k_smallest(
                l,
                r,
                r - l - k,
            )
        )

    # =========================================================
    # greedy by descending values
    # =========================================================

    def min_count_for_sum_ge(
        self,
        l: int,
        r: int,
        target: int,
    ) -> int:
        """
        a[l:r] から値の大きいものを優先して選び、
        総和を target 以上にするための最小個数を返す。

        不可能なら -1。

        値が非負であることを前提とする。
        """

        if target <= 0:
            return 0

        total = self.range_sum(
            l,
            r,
        )

        if total < target:
            return -1

        node = 1
        answer = 0

        while node < self.size:

            right = node * 2 + 1

            count, total = self._node_query(
                right,
                l,
                r,
            )

            if total >= target:
                node = right

            else:
                answer += count
                target -= total

                node *= 2

        value = self.values[node - self.size]

        answer += (
            target + value - 1
        ) // value

        return answer



