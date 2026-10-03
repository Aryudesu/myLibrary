def subsetZetaOr(N: int, data: dict[int, list[int]])->list:
    """
    部分集合ゼータ変換（bitwise OR）。

    data[key] に、key に対応する条件の部分集合maskを列挙する。

    戻り値 result[mask] は、
        sub ⊆ mask
    を満たすいずれかの sub が data[key] に存在する key を
    bit集合として保持する。

    つまり、
        result[mask] & (1 << key)
    が真なら、key に対応する条件のうち少なくとも1つが
    mask の部分集合として成立している。

    計算量:
        O(N * 2^N + dataの総要素数)

    key は 0-indexed を想定。
    """
    result = [0] * (1 << N)
    for key, values in data.items():
        for value in values:
            result[value] |= (1 << key)

    for mask in range(1 << N):
        for n in range(N):
            b = mask | (1 << n)
            result[b] |= result[mask]

    return result
