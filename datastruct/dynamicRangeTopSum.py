from array import array


class DynamicRangeTopSum:
    """
    一点更新 + 区間 [l, r) に対して、
    「大きい値から選んだとき、総和を k 以上にする最小個数」
    を求める平方分割ライブラリ。

    0-indexed / half-open [l, r)

    注意:
        座標圧縮を用いるため、将来 update で登場する値を
        update_values として初期化時にすべて渡す必要がある。

    計算量:
        構築:
            O(N sqrt(N)) 相当

        update(i, x):
            O(N / POSITION_BLOCK)

        min_count_to_reach(l, r, k):
            O(
                POSITION_BLOCK
                + M / VALUE_BLOCK
                + VALUE_BLOCK
            )

        M = 初期値 + 更新値の異なる値の個数

    Many Sweets Problem のように
    POSITION_BLOCK ≒ VALUE_BLOCK ≒ sqrt(N)
    とすると、おおむね O(sqrt(N)) / query。
    """

    def __init__(
        self,
        data: list[int],
        update_values=(),
        position_block_size: int = 500,
        value_block_size: int = 500,
    ):
        self.n = len(data)

        self.P = position_block_size
        self.V = value_block_size

        # --------------------------------------------------
        # 座標圧縮
        # --------------------------------------------------

        values = sorted(set(data) | set(update_values))

        self.values = values
        self.m = len(values)

        self.rank = {
            value: i
            for i, value in enumerate(values)
        }

        # A は圧縮後の値を持つ
        self.a = [
            self.rank[x]
            for x in data
        ]

        # --------------------------------------------------
        # ブロック数
        # --------------------------------------------------

        self.position_block_count = (
            self.n + self.P - 1
        ) // self.P

        self.value_block_count = (
            self.m + self.V - 1
        ) // self.V

        NB = self.position_block_count
        VB = self.value_block_count
        M = self.m

        # --------------------------------------------------
        # prefix_exact_count
        #
        # prefix_exact_count[b][v]
        #   = 先頭 b 個の「添字ブロック」に含まれる
        #     圧縮値 v の個数
        #
        # Python の list[list[int]] ではメモリが非常に重いため、
        # uint32 の一次元 array で保持。
        # --------------------------------------------------

        exact_count = array("I", [0]) * M

        # --------------------------------------------------
        # prefix_block_sum
        #
        # prefix_block_sum[b][g]
        #   = 先頭 b 個の添字ブロックにある要素のうち、
        #     値ブロック g に属する要素の総和
        #
        # prefix_block_count[b][g]
        #   = 同じ条件での個数
        # --------------------------------------------------

        block_sum = array("q", [0]) * VB
        block_count = array("I", [0]) * VB

        # --------------------------------------------------
        # prefix を構築
        #
        # Python で
        #
        # for value in range(M):
        #     next[value] = prev[value]
        #
        # とすると遅いので、array の slice copy を使う。
        # --------------------------------------------------

        for b in range(NB):

            exact_count.extend(
                exact_count[-M:]
            )

            block_sum.extend(
                block_sum[-VB:]
            )

            block_count.extend(
                block_count[-VB:]
            )

            exact_offset = (b + 1) * M
            block_offset = (b + 1) * VB

            left = b * self.P
            right = min(
                left + self.P,
                self.n,
            )

            for i in range(left, right):

                rk = self.a[i]

                value = values[rk]

                value_block = rk // self.V

                exact_count[
                    exact_offset + rk
                ] += 1

                block_sum[
                    block_offset + value_block
                ] += value

                block_count[
                    block_offset + value_block
                ] += 1

        self.exact_count = exact_count

        self.block_sum = block_sum
        self.block_count = block_count

        # --------------------------------------------------
        # クエリの端部分を一時的に集計する配列
        #
        # 毎回 O(M) で初期化すると意味がないので、
        # timestamp 方式で使った場所だけ有効とみなす。
        # --------------------------------------------------

        self.tmp_exact_count = [0] * M
        self.tmp_exact_mark = [0] * M

        self.tmp_block_sum = [0] * VB
        self.tmp_block_count = [0] * VB
        self.tmp_block_mark = [0] * VB

        self.query_id = 0

    # ==================================================
    # 一点更新
    # ==================================================

    def update(self, i: int, x: int) -> None:
        """
        A[i] = x

        0-indexed
        """

        new_rank = self.rank[x]
        old_rank = self.a[i]

        if old_rank == new_rank:
            return

        old_value = self.values[old_rank]
        new_value = x

        old_value_block = old_rank // self.V
        new_value_block = new_rank // self.V

        M = self.m
        VB = self.value_block_count

        # i が属する添字ブロック以降の prefix を更新
        start_block = i // self.P + 1

        exact_count = self.exact_count
        block_sum = self.block_sum
        block_count = self.block_count

        for b in range(
            start_block,
            self.position_block_count + 1,
        ):

            exact_offset = b * M

            exact_count[
                exact_offset + old_rank
            ] -= 1

            exact_count[
                exact_offset + new_rank
            ] += 1

            block_offset = b * VB

            block_sum[
                block_offset + old_value_block
            ] -= old_value

            block_sum[
                block_offset + new_value_block
            ] += new_value

            block_count[
                block_offset + old_value_block
            ] -= 1

            block_count[
                block_offset + new_value_block
            ] += 1

        self.a[i] = new_rank

    # ==================================================
    # Query
    # ==================================================

    def min_count_to_reach(
        self,
        l: int,
        r: int,
        k: int,
    ) -> int:
        """
        区間 A[l:r] から値を自由に選ぶ。

        選んだ値の総和を k 以上にするために必要な
        最小個数を返す。

        不可能なら -1。

        0-indexed / half-open [l, r)
        """

        if l >= r:
            return -1

        self.query_id += 1
        qid = self.query_id

        P = self.P
        V = self.V

        M = self.m
        VB = self.value_block_count

        values = self.values
        a = self.a

        tmp_exact_count = self.tmp_exact_count
        tmp_exact_mark = self.tmp_exact_mark

        tmp_block_sum = self.tmp_block_sum
        tmp_block_count = self.tmp_block_count
        tmp_block_mark = self.tmp_block_mark

        left_block = l // P
        right_block = (r - 1) // P

        # ----------------------------------------------
        # 左右の端部分を追加
        # ----------------------------------------------

        def add_boundary(i: int) -> None:

            rk = a[i]

            value = values[rk]

            value_block = rk // V

            if tmp_exact_mark[rk] != qid:

                tmp_exact_mark[rk] = qid

                tmp_exact_count[rk] = 1

            else:

                tmp_exact_count[rk] += 1

            if tmp_block_mark[value_block] != qid:

                tmp_block_mark[value_block] = qid

                tmp_block_sum[value_block] = value

                tmp_block_count[value_block] = 1

            else:

                tmp_block_sum[value_block] += value

                tmp_block_count[value_block] += 1

        # ----------------------------------------------
        # 中央部分について使う prefix の範囲
        #
        # prefix[high] - prefix[low]
        # ----------------------------------------------

        if left_block == right_block:

            for i in range(l, r):
                add_boundary(i)

            prefix_low = 0
            prefix_high = 0

        else:

            left_end = min(
                (left_block + 1) * P,
                self.n,
            )

            for i in range(l, left_end):
                add_boundary(i)

            right_start = right_block * P

            for i in range(right_start, r):
                add_boundary(i)

            # 完全に含まれる添字ブロック
            #
            # left_block + 1
            # ...
            # right_block - 1

            prefix_low = left_block + 1
            prefix_high = right_block

        # ----------------------------------------------
        # offset
        # ----------------------------------------------

        block_low_offset = (
            prefix_low * VB
        )

        block_high_offset = (
            prefix_high * VB
        )

        exact_low_offset = (
            prefix_low * M
        )

        exact_high_offset = (
            prefix_high * M
        )

        exact_count = self.exact_count

        block_sum = self.block_sum
        block_count = self.block_count

        answer = 0

        # ==================================================
        # 値ブロックを大きい方から見る
        # ==================================================

        for value_block in range(
            VB - 1,
            -1,
            -1,
        ):

            # ------------------------------------------
            # この値ブロックの総和
            # ------------------------------------------

            current_sum = (
                block_sum[
                    block_high_offset
                    + value_block
                ]
                -
                block_sum[
                    block_low_offset
                    + value_block
                ]
            )

            current_count = (
                block_count[
                    block_high_offset
                    + value_block
                ]
                -
                block_count[
                    block_low_offset
                    + value_block
                ]
            )

            # 左右端
            if (
                tmp_block_mark[value_block]
                == qid
            ):

                current_sum += (
                    tmp_block_sum[value_block]
                )

                current_count += (
                    tmp_block_count[value_block]
                )

            # ------------------------------------------
            # このブロックを全部食べても不足
            # ------------------------------------------

            if k > current_sum:

                k -= current_sum

                answer += current_count

                continue

            # ==================================================
            # この値ブロック内で答えが決まる
            # ==================================================

            value_left = (
                value_block * V
            )

            value_right = min(
                (value_block + 1) * V,
                M,
            ) - 1

            for rk in range(
                value_right,
                value_left - 1,
                -1,
            ):

                count = (
                    exact_count[
                        exact_high_offset + rk
                    ]
                    -
                    exact_count[
                        exact_low_offset + rk
                    ]
                )

                if tmp_exact_mark[rk] == qid:
                    count += tmp_exact_count[rk]

                if count == 0:
                    continue

                value = values[rk]

                current_sum = count * value

                if k > current_sum:

                    k -= current_sum

                    answer += count

                else:

                    # ceil(k / value)
                    answer += (
                        k + value - 1
                    ) // value

                    return answer

        return -1


N, Q = map(int, input().split())
A = list(map(int, input().split()))

queries = []
update_values = []

for _ in range(Q):

    c, x, l, r, k = map(
        int,
        input().split(),
    )

    queries.append(
        (c - 1, x, l - 1, r, k)
    )

    update_values.append(x)


ds = DynamicRangeTopSum(
    A,
    update_values,
    position_block_size=500,
    value_block_size=500,
)


ans = []

for c, x, l, r, k in queries:

    ds.update(c, x)

    ans.append(
        str(
            ds.min_count_to_reach(
                l,
                r,
                k,
            )
        )
    )

print("\n".join(ans))
