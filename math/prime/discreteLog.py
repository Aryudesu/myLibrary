from math import isqrt, gcd


def discreteLog(a: int, b: int, mod: int) -> int | None:
    """
    a^x ≡ b (mod mod) を満たす最小の非負整数 x を探す。

    前提:
        gcd(a, mod) = 1

    戻り値:
        解が存在すれば x
        存在しなければ None

    計算量:
        O(sqrt(mod))
    """
    if mod == 1:
        return 0

    a %= mod
    b %= mod

    if b == 1:
        return 0

    n = isqrt(mod) + 1

    # baby[a^r] = 最小の r
    baby: dict[int, int] = {}
    cur = 1
    for r in range(n):
        if cur not in baby:
            baby[cur] = r
        cur = cur * a % mod

    # a^(-n)
    a_inv_n = pow(pow(a, n, mod), -1, mod)

    cur = b
    answer = None

    for q in range(n + 1):
        if cur in baby:
            x = q * n + baby[cur]
            if pow(a, x, mod) == b:
                if answer is None or x < answer:
                    answer = x

        cur = cur * a_inv_n % mod

    return answer

