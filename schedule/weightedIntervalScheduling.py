from bisect import bisect_right
class WeightedIntervalScheduling:
    """
    半開区間 [l, r) の重み付き区間スケジューリング。
    重ならない区間を選んだときの重み和最大値を求める。

    - 端点が一致する [1,3), [3,5) は両方選べる
    - 重みは負でも可
    """

    def __init__(self):
        self.intervals = []

    def add(self, l: int, r: int, w: int) -> None:
        assert l <= r
        self.intervals.append((l, r, w))

    def solve(self) -> int:
        segs = sorted(self.intervals, key=lambda x: x[1])
        ends = [r for _, r, _ in segs]

        n = len(segs)
        dp = [0] * (n + 1)

        for i, (l, r, w) in enumerate(segs):
            # 終了時刻 <= l の最後の区間まで使える
            j = bisect_right(ends, l, 0, i)

            dp[i + 1] = max(
                dp[i],
                dp[j] + w
            )

        return dp[n]
