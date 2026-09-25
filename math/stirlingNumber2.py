class StirlingNumber2:
    """
    第二種スターリング数 S(n, k) を漸化式で前計算するクラス。

    S(n, k) = k * S(n - 1, k) + S(n - 1, k - 1)

    0 <= n <= maxN の全ての S(n, k) を保持するため、
    小さい maxN に対して多数のクエリを処理する用途向け。

    計算量:
        前計算: O(maxN^2)
        S(n, k): O(1)
    空間計算量:
        O(maxN^2)
    """

    def __init__(self, maxN: int = 1000, mod: int = 998244353):
        self.mod = mod
        self.M = maxN
        self.data = [[1]]
        self._makeData()

    def _makeData(self) -> None:
        if self.M >= 1:
            self.data.append([0, 1])

        for n in range(2, self.M + 1):
            prev = self.data[n - 1]
            row = [0]
            for k in range(1, n):
                value = k * prev[k] + prev[k - 1]
                if self.mod > 0:
                    value %= self.mod
                row.append(value)
            row.append(1)
            self.data.append(row)

    def S(self, n: int, k: int) -> int:
        """第二種スターリング数 S(n, k) を返す。"""
        assert 0 <= n <= self.M
        if k < 0 or n < k:
            return 0
        return self.data[n][k]


def stirlingNumber2Row(n: int, mod: int = 998244353) -> list[int]:
    """
    第二種スターリング数の第 n 行
    [S(n, 0), S(n, 1), ..., S(n, n)] を計算する。

    漸化式
        S(i, k) = k * S(i - 1, k) + S(i - 1, k - 1)
    を k の降順に更新することで、1 次元配列だけで計算する。

    固定した n に対する S(n, k) を全て必要とするが、
    それ以前の行を保持する必要がない場合に適している。

    計算量:
        O(n^2)
    空間計算量:
        O(n)
    """
    assert n >= 0

    dp = [0] * (n + 1)
    dp[0] = 1

    for i in range(1, n + 1):
        for k in range(i, 0, -1):
            value = k * dp[k] + dp[k - 1]
            if mod > 0:
                value %= mod
            dp[k] = value
        dp[0] = 0

    return dp


def stirlingNumber2(n: int, k: int, mod: int = 998244353) -> int:
    """
    第二種スターリング数 S(n, k) を単体で計算する。

    包除原理による公式
        S(n, k) = 1 / k! * sum((-1)^(k-i) * C(k, i) * i^n)
    を用いる。

    mod は素数、かつ k < mod を想定する。

    計算量:
        O(k log n)  (pow を含む)
    空間計算量:
        O(1)
    """
    if n < 0 or k < 0 or n < k:
        return 0
    if k == 0:
        return 1 if n == 0 else 0

    # C(k, i) と k! を逐次計算する。
    # comb = C(k, i)
    comb = 1
    fact = 1
    total = 0

    for i in range(k + 1):
        term = comb * pow(i, n, mod) % mod
        if (k - i) & 1:
            total -= term
        else:
            total += term
        total %= mod

        if i < k:
            # C(k, i+1) = C(k, i) * (k-i) / (i+1)
            comb = comb * (k - i) % mod
            comb = comb * pow(i + 1, mod - 2, mod) % mod
            fact = fact * (i + 1) % mod

    return total * pow(fact, mod - 2, mod) % mod
