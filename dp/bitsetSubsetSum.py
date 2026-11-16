class BitsetSubsetSum:
    """非負整数の部分和について、到達可能性をビット集合で管理する。

    bit s が 1 なら、追加済みの要素から部分和 s を作れる。
    add のみ対応（要素の削除・部分集合の復元・通り数計算は非対応）。

    max_sum を指定すると、それより大きい部分和は保存しない。
    問い合わせは保存している範囲内での結果を返す。
    """

    def __init__(self, max_sum: int | None = None):
        if max_sum is not None and max_sum < 0:
            raise ValueError("max_sum must be non-negative")
        self.max_sum = max_sum
        self.bits = 1  # 空集合による部分和 0
        self._mask = (1 << (max_sum + 1)) - 1 if max_sum is not None else None

    def add(self, x: int) -> None:
        """重さ x の要素を1個追加する。x >= 0。"""
        if x < 0:
            raise ValueError("x must be non-negative")
        self.bits |= self.bits << x
        if self._mask is not None:
            self.bits &= self._mask

    def contains(self, s: int) -> bool:
        """部分和 s を作れるか。保存範囲外は False。"""
        if s < 0 or (self.max_sum is not None and s > self.max_sum):
            return False
        return bool((self.bits >> s) & 1)

    def __contains__(self, s: int) -> bool:
        return self.contains(s)

    def max_leq(self, x: int) -> int | None:
        """保存済みの部分和のうち x 以下の最大値（なければ None）。"""
        if x < 0:
            return None
        if self.max_sum is not None:
            x = min(x, self.max_sum)
        lower = self.bits & ((1 << (x + 1)) - 1)
        return lower.bit_length() - 1 if lower else None

    def min_geq(self, x: int) -> int | None:
        """保存済みの部分和のうち x 以上の最小値（なければ None）。"""
        x = max(x, 0)
        if self.max_sum is not None and x > self.max_sum:
            return None
        upper = self.bits >> x
        if not upper:
            return None
        lowbit = upper & -upper
        return x + lowbit.bit_length() - 1


if __name__ == "__main__":
    # AWC0201 E: 荷物を2人に分配し、重量差を最小化
    N = int(input())
    A = list(map(int, input().split()))
    total = sum(A)
    dp = BitsetSubsetSum(total // 2)
    for a in A:
        dp.add(a)
    best = dp.max_leq(total // 2)
    print(total - 2 * best)
