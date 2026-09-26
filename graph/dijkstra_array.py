from heapq import heappop, heappush

INF = 10**30


def dijkstra(
    graph: list[list[tuple[int, int]]],
    start: int,
    inf: int = INF,
) -> list[int]:
    """
    配列ベースの隣接リストに対する Dijkstra 法。

    Args:
        graph:
            graph[v] = [(to, cost), ...] の形式。
            辺重みは非負であること。
        start:
            始点。
        inf:
            到達不能頂点の距離として用いる値。

    Returns:
        start から各頂点への最短距離。

    計算量:
        O((N + M) log N)
    """
    n = len(graph)
    assert 0 <= start < n

    dist = [inf] * n
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, v = heappop(pq)
        if d != dist[v]:
            continue

        for to, cost in graph[v]:
            nd = d + cost
            if nd < dist[to]:
                dist[to] = nd
                heappush(pq, (nd, to))

    return dist


def dijkstra_with_prev(
    graph: list[list[tuple[int, int]]],
    start: int,
    inf: int = INF,
) -> tuple[list[int], list[int]]:
    """
    最短距離と最短路復元用の直前頂点を返す Dijkstra 法。

    Returns:
        (dist, prev)
        prev[v] は最短路上で v の直前にある頂点。
        start および到達不能頂点では -1。
    """
    n = len(graph)
    assert 0 <= start < n

    dist = [inf] * n
    prev = [-1] * n
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, v = heappop(pq)
        if d != dist[v]:
            continue

        for to, cost in graph[v]:
            nd = d + cost
            if nd < dist[to]:
                dist[to] = nd
                prev[to] = v
                heappush(pq, (nd, to))

    return dist, prev


def restore_path(prev: list[int], start: int, goal: int) -> list[int]:
    """
    dijkstra_with_prev が返した prev から start -> goal の経路を復元する。

    到達不能の場合は空リストを返す。
    """
    n = len(prev)
    assert 0 <= start < n
    assert 0 <= goal < n

    if start == goal:
        return [start]
    if prev[goal] == -1:
        return []

    path = []
    v = goal

    while v != -1:
        path.append(v)
        if v == start:
            path.reverse()
            return path
        v = prev[v]

    return []
