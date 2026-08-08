from bisect import bisect_left


class DynamicRangeTopSum:
    """
    動的配列に対して以下を行うデータ構造。

    - point_set(i, x)
        A[i] = x

    - min_count_to_sum(l, r, k)
        A[l:r] から値の大きいものを選び、
        合計を k 以上にするための最小個数を返す。
        不可能なら -1。

    構造:
        値方向 Fenwick Tree
            ×
        添字方向 Fenwick Tree

    注意:
        更新で現れる値を事前にすべて与える offline 構築。

    計算量:
        構築:
            O((N + U) log V + S)
            ※ S は内部Fenwickの総サイズ

        更新:
            O(log V log N)

        クエリ:
            O(log V log N)

    0-indexed
    区間は [l, r)
    """

    def __init__(
        self,
        A: list[int],
        updates: list[tuple[int, int]],
    ):
        self.N = len(A)
        self.A = A[:]

        # -------------------------
        # 値を降順に座標圧縮
        # -------------------------

        values = A[:]

        for _, x in updates:
            values.append(x)

        values = sorted(set(values), reverse=True)

        self.values = values
        self.M = len(values)

        rank = {
            x: i + 1
            for i, x in enumerate(values)
        }

        self.rank = rank

        current_rank = [
            rank[x]
            for x in A
        ]

        self.current_rank = current_rank

        # --------------------------------------------------
        # 各添字が将来到達する可能性のある rank を収集
        # --------------------------------------------------

        candidates = [
            [current_rank[i]]
            for i in range(self.N)
        ]

        for i, x in updates:
            candidates[i].append(rank[x])

        # --------------------------------------------------
        # 外側Fenwickノードごとに
        # 「そこへ来る可能性のある添字」を列挙
        # --------------------------------------------------

        positions = [
            []
            for _ in range(self.M + 1)
        ]

        M = self.M

        for i, ranks in enumerate(candidates):

            if len(ranks) >= 2:
                ranks = set(ranks)

            for r in ranks:

                p = r

                while p <= M:

                    positions[p].append(i)

                    p += p & -p

        # i の昇順に追加しているので既にソート済み。
        # 同一 i が複数rank経由で同じFenwickノードに
        # 入ることがあるので隣接重複だけ消す。

        for p in range(1, M + 1):

            arr = positions[p]

            if not arr:
                continue

            res = []

            last = -1

            for x in arr:

                if x != last:

                    res.append(x)

                    last = x

            positions[p] = res

        self.positions = positions

        # --------------------------------------------------
        # 内側Fenwickを全部flatに持つ
        #
        # Pythonでは
        #
        #     bit[node] = [...]
        #
        # と大量のlistを作るより、
        # 一本の配列 + offset の方が軽い。
        # --------------------------------------------------

        offsets = [0] * (M + 1)

        total_size = 0

        for p in range(1, M + 1):

            offsets[p] = total_size

            total_size += len(positions[p]) + 1

        self.offsets = offsets

        bit_count = [0] * total_size
        bit_sum = [0] * total_size

        self.bit_count = bit_count
        self.bit_sum = bit_sum

        # --------------------------------------------------
        # 初期状態を O(内部配列総サイズ) で構築
        #
        # N回 point_add すると重いので、
        # raw arrayを作ってからFenwick化する。
        # --------------------------------------------------

        for p in range(1, M + 1):

            ps = positions[p]

            if not ps:
                continue

            offset = offsets[p]

            # 外側Fenwick p が担当するrank区間
            low = p - (p & -p) + 1
            high = p

            # raw array
            for j, i in enumerate(ps, 1):

                r = current_rank[i]

                if low <= r <= high:

                    bit_count[offset + j] = 1
                    bit_sum[offset + j] = A[i]

            # linear Fenwick build
            size = len(ps)

            for j in range(1, size + 1):

                parent = j + (j & -j)

                if parent <= size:

                    bit_count[offset + parent] += (
                        bit_count[offset + j]
                    )

                    bit_sum[offset + parent] += (
                        bit_sum[offset + j]
                    )

        # Fenwick lower_bound用
        self.top_bit = 1 << (M.bit_length() - 1)

    # =========================================================
    # inner Fenwick
    # =========================================================

    def _add_node(
        self,
        node: int,
        index: int,
        delta_count: int,
        delta_sum: int,
    ) -> None:

        ps = self.positions[node]

        j = bisect_left(ps, index) + 1

        size = len(ps)
        offset = self.offsets[node]

        bit_count = self.bit_count
        bit_sum = self.bit_sum

        while j <= size:

            if delta_count:

                bit_count[offset + j] += delta_count

            bit_sum[offset + j] += delta_sum

            j += j & -j

    def _range_node(
        self,
        node: int,
        l: int,
        r: int,
    ) -> tuple[int, int]:

        ps = self.positions[node]

        left = bisect_left(ps, l)
        right = bisect_left(ps, r)

        offset = self.offsets[node]

        bit_count = self.bit_count
        bit_sum = self.bit_sum

        count = 0
        total = 0

        j = right

        while j:

            count += bit_count[offset + j]
            total += bit_sum[offset + j]

            j -= j & -j

        j = left

        while j:

            count -= bit_count[offset + j]
            total -= bit_sum[offset + j]

            j -= j & -j

        return count, total

    # =========================================================
    # update
    # =========================================================

    def point_set(
        self,
        index: int,
        x: int,
    ) -> None:

        old = self.A[index]

        if old == x:
            return

        old_rank = self.current_rank[index]
        new_rank = self.rank[x]

        M = self.M

        # 古い値を削除
        p = old_rank

        while p <= M:

            self._add_node(
                p,
                index,
                -1,
                -old,
            )

            p += p & -p

        # 新しい値を追加
        p = new_rank

        while p <= M:

            self._add_node(
                p,
                index,
                1,
                x,
            )

            p += p & -p

        self.A[index] = x
        self.current_rank[index] = new_rank

    # =========================================================
    # query
    # =========================================================

    def min_count_to_sum(
        self,
        l: int,
        r: int,
        k: int,
    ) -> int:

        """
        A[l:r] から好きな要素を選び、
        合計を k 以上にする最小個数。

        不可能なら -1。
        """

        idx = 0

        accumulated_count = 0
        accumulated_sum = 0

        step = self.top_bit
        M = self.M

        # Fenwick lower_bound
        #
        # idx:
        #   「ここまで全部食べても k 未満」
        #   となる最大rank

        while step:

            nxt = idx + step

            if nxt <= M:

                count, total = self._range_node(
                    nxt,
                    l,
                    r,
                )

                if accumulated_sum + total < k:

                    idx = nxt

                    accumulated_sum += total
                    accumulated_count += count

            step >>= 1

        # 全部食べても足りない
        if idx == M:
            return -1

        # rank = idx+1 の値
        #
        # values は0-indexなので values[idx]
        value = self.values[idx]

        remain = k - accumulated_sum

        need = (
            remain + value - 1
        ) // value

        return accumulated_count + need


import sys


def main():
    input = sys.stdin.readline

    N, Q = map(int, input().split())

    A = list(map(int, input().split()))

    queries = []
    updates = []

    for _ in range(Q):

        c, x, l, r, k = map(
            int,
            input().split(),
        )

        c -= 1
        l -= 1

        queries.append(
            (c, x, l, r, k)
        )

        updates.append(
            (c, x)
        )

    ds = DynamicRangeTopSum(
        A,
        updates,
    )

    ans = []

    for c, x, l, r, k in queries:

        ds.point_set(
            c,
            x,
        )

        res = ds.min_count_to_sum(
            l,
            r,
            k,
        )

        ans.append(str(res))

    print("\n".join(ans))


if __name__ == "__main__":
    main()

