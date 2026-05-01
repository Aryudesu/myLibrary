def sum_floor_linear_denominator(A: int, b: int, c: int, l: int, r: int) -> int:
    """
    sum_{i=l}^r floor(A / (b*i + c))
    b > 0, b*i+c > 0 を想定
    """
    res = 0
    i = l
    while i <= r:
        den = b * i + c
        q = A // den
        if q == 0:
            break

        # A // (b*j+c) == q となる最大 j
        ni = (A // q - c) // b
        ni = min(ni, r)

        res += q * (ni - i + 1)
        i = ni + 1

    return res
