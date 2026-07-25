from math import isqrt, gcd


def multiplicativeOrder(a: int, mod: int) -> int | None:
    """
    a^x ≡ 1 (mod mod) を満たす最小の正整数 x を返す。

    前提:
        gcd(a, mod) = 1

    計算量:
        O(sqrt(mod))
    """
    if mod == 1:
        return 1

    a %= mod

    if gcd(a, mod) != 1:
        return None

    m = isqrt(mod) + 1

    # a^j を記録する。
    # 同じ値が複数回現れた場合、候補 im-j を小さくするため
    # 最大の j を保存する。
    baby: dict[int, int] = {}

    cur = 1
    for j in range(m):
        baby[cur] = j
        cur = cur * a % mod

    # cur = a^m
    giant_step = cur
    cur = giant_step
    answer: int | None = None

    for i in range(1, m + 1):
        # a^(im) = a^j → a^(im-j) = 1
        if cur in baby:
            j = baby[cur]
            x = i * m - j
            if x > 0 and pow(a, x, mod) == 1:
                if answer is None or x < answer:
                    answer = x
        cur = cur * giant_step % mod
    return answer


# ABC222 G
def calc(k: int) -> int:
    # 222...2 は5の倍数にはならない
    if k % 5 == 0:
        return -1
    mod = 9 * k // gcd(k, 2)
    order = multiplicativeOrder(10, mod)
    if order is None:
        return -1
    return order


T = int(input())

result = []
for _ in range(T):
    K = int(input())
    result.append(calc(K))

print(*result, sep="\n")
