def weightedMedian(values, weights):
    """重み付き中央値（最小の最適解）を返す。

    sum(weights[i] * abs(x - values[i])) を最小にする x を返す。
    values は大小比較・減算が可能な数値（Fraction 等も可）。
    weights は非負の数値で、総和は正であること。

    戻り値は入力の values のいずれか。偶数個相当で最適区間が
    存在する場合は、その左端を返す。

    計算量: O(N log N)、追加空間: O(N)。
    """
    if len(values) != len(weights):
        raise ValueError("values and weights must have the same length")
    if not values:
        raise ValueError("values must not be empty")
    if any(w < 0 for w in weights):
        raise ValueError("weights must be non-negative")

    pairs = sorted((v, w) for v, w in zip(values, weights) if w > 0)
    total = sum(w for _, w in pairs)
    if total <= 0:
        raise ValueError("sum of weights must be positive")

    prefix = 0
    for value, weight in pairs:
        prefix += weight
        if prefix * 2 >= total:
            return value

    raise RuntimeError("unreachable")
