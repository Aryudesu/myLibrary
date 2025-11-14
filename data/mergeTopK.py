def mergeTopK(A: list[int], B: list[int], K: int = 20) -> list[int]:
    """配列AとBのマージ結果のうち，上位K個の配列を返却します．"""
    i = j = 0
    n, m = len(A), len(B)
    res = []

    while len(res) < K and (i < n or j < m):
        if j >= m or (i < n and A[i] >= B[j]):
            res.append(A[i])
            i += 1
        else:
            res.append(B[j])
            j += 1

    return res
