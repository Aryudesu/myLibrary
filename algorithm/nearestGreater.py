def nearestGreaterIndices(A: list[int]) -> tuple[list[int], list[int]]:
    """
    各要素について、左右で最も近い「自分より大きい要素」の index を求める。

    Args:
        A:
            対象の配列。

    Returns:
        (left, right)

        left[i]:
            i より左で最も近い j < i かつ A[j] > A[i] を満たす j。
            存在しない場合は -1。

        right[i]:
            i より右で最も近い j > i かつ A[j] > A[i] を満たす j。
            存在しない場合は len(A)。

    計算量:
        O(N)

    Note:
        単調スタックを用いる。
        等しい値は「大きい」とみなさないため、A[stack[-1]] <= A[i] の間 pop する。
    """
    N = len(A)

    left = [-1] * N
    right = [N] * N

    stack: list[int] = []

    for i, x in enumerate(A):
        while stack and A[stack[-1]] <= x:
            stack.pop()

        if stack:
            left[i] = stack[-1]

        stack.append(i)

    stack.clear()

    for i in range(N - 1, -1, -1):
        x = A[i]

        while stack and A[stack[-1]] <= x:
            stack.pop()

        if stack:
            right[i] = stack[-1]

        stack.append(i)

    return left, right
