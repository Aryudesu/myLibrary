from collections import defaultdict
from typing import Callable, Hashable


class DigitDP:
    """
    0 <= x <= n を base 進数で桁DPする汎用フレームワーク。

    base:
        基数。2なら二進数、10なら十進数。

    mod:
        None なら通常整数。
        指定した場合は mod で管理。
    """

    def __init__(
        self,
        n: int,
        base: int = 10,
        mod: int | None = None,
    ):
        assert base >= 2

        self.base = base
        self.mod = mod
        self.digits = self._to_digits(n)

    def _to_digits(self, n: int) -> list[int]:
        if n == 0:
            return [0]

        digits = []

        while n:
            digits.append(n % self.base)
            n //= self.base

        return digits[::-1]

    def count(
        self,
        init_state: Hashable,
        transition: Callable[[Hashable, int, bool], Hashable | None],
        accept: Callable[[Hashable, bool], bool],
    ) -> int:

        dp = {(init_state, True, False): 1}

        for limit_digit in self.digits:
            ndp = defaultdict(int)

            for (state, tight, started), cnt in dp.items():
                upper = limit_digit if tight else self.base - 1

                for d in range(upper + 1):
                    ntight = tight and (d == limit_digit)
                    nstarted = started or d != 0

                    nstate = transition(state, d, nstarted)

                    if nstate is None:
                        continue

                    key = (nstate, ntight, nstarted)
                    ndp[key] += cnt

                    if self.mod is not None:
                        ndp[key] %= self.mod

            dp = ndp

        ans = 0

        for (state, _, started), cnt in dp.items():
            if accept(state, started):
                ans += cnt

                if self.mod is not None:
                    ans %= self.mod

        return ans

    def sum(
        self,
        init_state: Hashable,
        transition: Callable[[Hashable, int, bool], Hashable | None],
        accept: Callable[[Hashable, bool], bool],
    ) -> int:
        """
        条件を満たす x の総和を返す。

        各DP状態について
            cnt   : その状態に到達する数の個数
            total : その状態に到達する数そのものの総和
        を管理する。
        """

        # (state, tight, started) -> (個数, 総和)
        dp = {
            (init_state, True, False): (1, 0)
        }

        for limit_digit in self.digits:
            ndp = {}

            for (state, tight, started), (cnt, total) in dp.items():
                upper = limit_digit if tight else self.base - 1

                for d in range(upper + 1):
                    ntight = tight and (d == limit_digit)
                    nstarted = started or d != 0

                    nstate = transition(state, d, nstarted)

                    if nstate is None:
                        continue

                    key = (nstate, ntight, nstarted)

                    # 既存の数 x に d を付ける
                    #
                    # x -> x * base + d
                    #
                    # よって総和は
                    # total * base + d * cnt
                    add_sum = total * self.base + d * cnt

                    old_cnt, old_sum = ndp.get(key, (0, 0))

                    new_cnt = old_cnt + cnt
                    new_sum = old_sum + add_sum

                    if self.mod is not None:
                        new_cnt %= self.mod
                        new_sum %= self.mod

                    ndp[key] = (new_cnt, new_sum)

            dp = ndp

        ans = 0

        for (state, _, started), (_, total) in dp.items():
            if accept(state, started):
                ans += total

                if self.mod is not None:
                    ans %= self.mod

        return ans


A, B = map(int, input().split())

def transition(state, d, started):
    if not started:
        return state
    return state or d == 4 or d == 9

def accept(state, started):
    return started and state

dpB = DigitDP(B)
R = dpB.count(False, transition, accept)
dpA = DigitDP(A-1)
L = dpA.count(False, transition, accept)
print(R-L)
