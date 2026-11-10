"""最小費用で整数区間 [1, N] を覆う（重複可）。"""

from math import inf


def minCostIntervalCover(n, intervals, restore=False):
    """閉区間 (l, r, cost) の一部を選び [1, n] を覆う最小費用を求める。

    各区間は高々1回選べ、重複してもよい。費用は非負。
    選択不可能なら -1 を返す。

    restore=False: 最小費用を返す。
    restore=True: (最小費用, 選んだ区間の0-indexed入力番号リスト)
                  を返す。不可能な場合は (-1, [])。

    n, m に対する計算量: O(n + m log m + m log n)、空間 O(n + m)。
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    items = []
    for i, (l, r, cost) in enumerate(intervals):
        if not 1 <= l <= r <= n:
            raise ValueError("interval must satisfy 1 <= l <= r <= n")
        if cost < 0:
            raise ValueError("cost must be non-negative")
        items.append((r, l, cost, i))

    if n == 0:
        return (0, []) if restore else 0

    items.sort()
    size = 1
    while size < n + 1:
        size *= 2
    identity = (inf, -1)
    tree = [identity] * (2 * size)
    tree[size] = (0, 0)
    for k in range(size - 1, 0, -1):
        tree[k] = min(tree[2 * k], tree[2 * k + 1])

    def query(left, right):
        """dp[left:right] の (最小費用, 到達座標)。"""
        left += size
        right += size
        result = identity
        while left < right:
            if left & 1:
                result = min(result, tree[left])
                left += 1
            if right & 1:
                right -= 1
                result = min(result, tree[right])
            left //= 2
            right //= 2
        return result

    parent = [None] * (n + 1) if restore else None
    for r, l, cost, original_index in items:
        best, prev = query(l - 1, r)
        candidate = best + cost
        if candidate < tree[size + r][0]:
            p = size + r
            tree[p] = (candidate, r)
            while p > 1:
                p //= 2
                tree[p] = min(tree[2 * p], tree[2 * p + 1])
            if restore:
                parent[r] = (prev, original_index)

    answer = tree[size + n][0]
    if answer == inf:
        return (-1, []) if restore else -1
    if not restore:
        return answer

    chosen = []
    pos = n
    while pos:
        prev, original_index = parent[pos]
        chosen.append(original_index)
        pos = prev
    chosen.reverse()
    return answer, chosen
