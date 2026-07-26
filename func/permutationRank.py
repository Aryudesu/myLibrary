def permutationRank(P: list[int]) -> int:
    """順列Pの辞書順順位を0-indexedで返す"""
    N = len(P)

    factorial = [1] * (N + 1)
    for i in range(1, N + 1):
        factorial[i] = factorial[i - 1] * i

    unused = list(range(1, N + 1))
    rank = 0

    for i, x in enumerate(P):
        smaller = unused.index(x)
        rank += smaller * factorial[N - 1 - i]
        unused.pop(smaller)

    return rank
