from collections import defaultdict
from typing import Callable, Hashable


class BigDigitDP:
    """
    0 <= x <= N の整数 x について桁DPする。
    N は巨大な10進整数を文字列で受け取る。

    例:
        N = "10000000000000000000000000000000000000000"

    state:
        Hashable なら何でもよい。

    mod:
        None なら通常の整数で管理する。
        整数を指定した場合は、その mod で管理する。

    leading zero 中は started=False として扱う。
    """

    def __init__(
        self,
        n: str,
        mod: int | None = None,
    ):
        assert isinstance(n, str)
        assert n
        assert n.isdigit()

        # "000123" のような入力も一応許容
        n = n.lstrip("0") or "0"

        self.digits = [ord(c) - ord("0") for c in n]
        self.mod = mod

    def count(
        self,
        init_state: Hashable,
        transition: Callable[[Hashable, int, bool], Hashable | None],
        accept: Callable[[Hashable, bool], bool],
    ) -> int:
        """
        条件を満たす整数 x の個数を返す。

        transition(state, digit, started) -> next_state or None

        state:
            現在の状態

        digit:
            今置く数字 (0～9)

        started:
            この digit を置いた後、
            leading zero を抜けて実際の整数が始まっているか

        None:
            この遷移を禁止する

        accept(state, started):
            最終状態を答えに含めるか
        """

        # (state, tight, started) -> 個数
        dp = {
            (init_state, True, False): 1
        }

        for limit_digit in self.digits:
            ndp = defaultdict(int)

            for (state, tight, started), cnt in dp.items():
                upper = limit_digit if tight else 9

                for d in range(upper + 1):
                    ntight = tight and (d == limit_digit)
                    nstarted = started or (d != 0)

                    nstate = transition(
                        state,
                        d,
                        nstarted,
                    )

                    if nstate is None:
                        continue

                    key = (
                        nstate,
                        ntight,
                        nstarted,
                    )

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

    def sum_values(
        self,
        init_state: Hashable,
        transition: Callable[[Hashable, int, bool], Hashable | None],
        accept: Callable[[Hashable, bool], bool],
    ) -> int:
        """
        条件を満たす整数 x 自身の総和を返す。

        内部では各状態について

            count:
                その状態に到達する整数の個数

            total:
                その状態に到達する整数の総和

        を同時に管理する。

        既存の数 x に数字 d を付けると

            x -> 10x + d

        なので、総和は

            total -> 10 * total + d * count

        と更新できる。
        """

        # (state, tight, started) -> (個数, 値の総和)
        dp = {
            (init_state, True, False): (1, 0)
        }

        for limit_digit in self.digits:
            ndp = {}

            for (state, tight, started), (cnt, total) in dp.items():
                upper = limit_digit if tight else 9

                for d in range(upper + 1):
                    ntight = tight and (d == limit_digit)
                    nstarted = started or (d != 0)

                    nstate = transition(
                        state,
                        d,
                        nstarted,
                    )

                    if nstate is None:
                        continue

                    key = (
                        nstate,
                        ntight,
                        nstarted,
                    )

                    add_cnt = cnt
                    add_sum = total * 10 + d * cnt

                    old_cnt, old_sum = ndp.get(
                        key,
                        (0, 0),
                    )

                    new_cnt = old_cnt + add_cnt
                    new_sum = old_sum + add_sum

                    if self.mod is not None:
                        new_cnt %= self.mod
                        new_sum %= self.mod

                    ndp[key] = (
                        new_cnt,
                        new_sum,
                    )

            dp = ndp

        ans = 0

        for (state, _, started), (_, total) in dp.items():
            if accept(state, started):
                ans += total

                if self.mod is not None:
                    ans %= self.mod

        return ans

    def count_and_sum_values(
        self,
        init_state: Hashable,
        transition: Callable[[Hashable, int, bool], Hashable | None],
        accept: Callable[[Hashable, bool], bool],
    ) -> tuple[int, int]:
        """
        条件を満たす整数について

            (個数, 値の総和)

        を同時に返す。
        """

        dp = {
            (init_state, True, False): (1, 0)
        }

        for limit_digit in self.digits:
            ndp = {}

            for (state, tight, started), (cnt, total) in dp.items():
                upper = limit_digit if tight else 9

                for d in range(upper + 1):
                    ntight = tight and (d == limit_digit)
                    nstarted = started or (d != 0)

                    nstate = transition(
                        state,
                        d,
                        nstarted,
                    )

                    if nstate is None:
                        continue

                    key = (
                        nstate,
                        ntight,
                        nstarted,
                    )

                    add_sum = total * 10 + d * cnt

                    old_cnt, old_sum = ndp.get(
                        key,
                        (0, 0),
                    )

                    new_cnt = old_cnt + cnt
                    new_sum = old_sum + add_sum

                    if self.mod is not None:
                        new_cnt %= self.mod
                        new_sum %= self.mod

                    ndp[key] = (
                        new_cnt,
                        new_sum,
                    )

            dp = ndp

        ans_cnt = 0
        ans_sum = 0

        for (state, _, started), (cnt, total) in dp.items():
            if accept(state, started):
                ans_cnt += cnt
                ans_sum += total

                if self.mod is not None:
                    ans_cnt %= self.mod
                    ans_sum %= self.mod

        return ans_cnt, ans_sum

MOD = 1_000_000_007
D = int(input())
N = input()

def transition(state, d, started):
    if not started:
        return state
    return (state + d) % D

def accept(state, started):
    return started and state == 0

dp = BigDigitDP(N, mod=MOD)
print(dp.count(0, transition, accept))
