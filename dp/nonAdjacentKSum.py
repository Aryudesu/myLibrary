import heapq


def minNonAdjacentKSum(A: list[int], K: int) -> int:
    """
    配列 A から隣り合わない要素をちょうど K 個選んだときの
    合計値の最小値を求める。

    Args:
        A:
            対象の配列。
        K:
            選ぶ要素数。

    Returns:
        条件を満たす K 個の要素の合計値の最小値。

    Raises:
        ValueError:
            K 個の要素を隣り合わないように選べない場合。

    計算量:
        O((N + K) log N)

    Note:
        現在選ぶ要素を x、その左右の要素を l, r としたとき、
        x を l, r に選び直す追加コスト

            l + r - x

        を新しい要素として残す「後悔貪欲」で計算する。
        heap と双方向連結リストを用いて縮約を高速に行う。
    """
    N = len(A)

    if K < 0 or K > (N + 1) // 2:
        raise ValueError("cannot select K non-adjacent elements")

    if K == 0:
        return 0

    INF = float("inf")

    # 0, N + 1 を番兵とする。
    data: list[int | float] = [INF] + A[:] + [INF]
    pre = [i - 1 for i in range(N + 2)]
    nxt = [i + 1 for i in range(N + 2)]

    q = [(A[i - 1], i) for i in range(1, N + 1)]
    heapq.heapify(q)

    ans = 0

    for _ in range(K):
        while True:
            value, i = heapq.heappop(q)
            if data[i] == value:
                break

        ans += value

        left = pre[i]
        right = nxt[i]

        # i を選んだ状態から、left と right を選ぶ状態へ
        # 後から変更するための差分を i に持たせる。
        data[i] = data[left] + data[right] - value
        heapq.heappush(q, (data[i], i))

        # left, right は i と隣接するため縮約する。
        if left != 0:
            data[left] = INF
            left = pre[left]

        if right != N + 1:
            data[right] = INF
            right = nxt[right]

        pre[i] = left
        nxt[left] = i
        nxt[i] = right
        pre[right] = i

    return int(ans)


def maxNonAdjacentKSum(A: list[int], K: int) -> int:
    """
    配列 A から隣り合わない要素をちょうど K 個選んだときの
    合計値の最大値を求める。

    Args:
        A:
            対象の配列。
        K:
            選ぶ要素数。

    Returns:
        条件を満たす K 個の要素の合計値の最大値。

    Raises:
        ValueError:
            K 個の要素を隣り合わないように選べない場合。

    計算量:
        O((N + K) log N)
    """
    return -minNonAdjacentKSum([-x for x in A], K)
