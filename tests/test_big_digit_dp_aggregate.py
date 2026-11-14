"""BigDigitDP.aggregate の動作確認（unittest）。"""
import unittest

from dp.bigDigitDP import BigDigitDP

MOD = 10**9 + 7


def count_smooth_substrings(n: str, d: int) -> int:
    """AWC0200 M の評価値を集計する aggregate() の使用例。"""

    def transition(prev, digit, started):
        return digit if started else -1

    def update(prev, digit, started, values):
        count, total, zero, smooth = values
        if not started:
            return values
        if prev == -1:
            return (count, total + count, 0, count)

        extended = smooth if abs(prev - digit) <= d else 0
        next_zero = count + zero if digit == 0 else 0
        next_smooth = (
            extended if digit == 0 else count + zero + extended
        )
        return (
            count,
            total + next_zero + next_smooth,
            next_zero,
            next_smooth,
        )

    _, answer, _, _ = BigDigitDP(n, mod=MOD).aggregate(
        -1,
        transition,
        update,
        lambda _state, started: started,
        initial=(1, 0, 0, 0),
    )
    return answer


def brute_force(n: int, d: int) -> int:
    result = 0
    for number in range(1, n + 1):
        s = str(number)
        for left in range(len(s)):
            for right in range(left + 1, len(s) + 1):
                v = str(int(s[left:right]))
                if all(
                    abs(int(v[i]) - int(v[i + 1])) <= d
                    for i in range(len(v) - 1)
                ):
                    result += 1
    return result


class TestBigDigitDPAggregate(unittest.TestCase):
    def test_smooth_substring_examples(self):
        cases = [
            ("20", 1, 34),
            ("101", 0, 206),
            ("3141592653589793238462643383279", 2, 584892474),
            (
                "12345678901234567890123456789012345678901234567890"
                "123456789012345678901234567890",
                4,
                940477512,
            ),
            ("1", 9, 1),
        ]
        for n, d, expected in cases:
            with self.subTest(n=n, d=d):
                self.assertEqual(count_smooth_substrings(n, d), expected)

    def test_against_brute_force(self):
        for d in range(10):
            for n in range(1, 101):
                with self.subTest(n=n, d=d):
                    self.assertEqual(count_smooth_substrings(str(n), d), brute_force(n, d))

    def test_count_and_sum(self):
        # 全整数の (個数, 数値の和) を集計
        for n in range(41):
            dp = BigDigitDP(str(n))
            result = dp.aggregate(
                0,
                lambda state, digit, started: state,
                lambda state, digit, started, v: (v[0], 10 * v[1] + digit * v[0]),
                lambda state, started: True,
            )
            self.assertEqual(result, (n + 1, n * (n + 1) // 2))

    def test_mod_and_rejected_transition(self):
        dp = BigDigitDP("500", mod=7)
        count, score = dp.aggregate(
            0,
            lambda state, digit, started: (
                None if started and digit == 7 else state
            ),
            lambda state, digit, started, values: (
                values[0], values[1] + int(started) * values[0]
            ),
            lambda state, started: started,
        )
        expected = [x for x in range(1, 501) if "7" not in str(x)]
        self.assertEqual(count, len(expected) % 7)
        self.assertEqual(score, sum(len(str(x)) for x in expected) % 7)

    def test_invalid_width(self):
        with self.assertRaises(ValueError):
            BigDigitDP("9").aggregate(
                None,
                lambda state, digit, started: state,
                lambda state, digit, started, values: (1, 2),
                lambda state, started: True,
                initial=(1,),
            )


if __name__ == "__main__":
    unittest.main()
