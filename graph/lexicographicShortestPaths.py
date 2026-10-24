from collections import deque


def lexicographicShortestPaths(
    graph: list[list[tuple[int, int]]],
    start: int,
    order: str = "min",
) -> tuple[list[int], list[int], list[int], list[int]]:
    """
    最短辺数の経路のうち、辺ラベル列が辞書順最小/最大となる経路を求める。

    Args:
        graph:
            graph[v] = [(to, label), ...] の形式の有向グラフ。
            label は比較可能な整数。多重辺・自己ループも可。
        start:
            始点（0-indexed）。
        order:
            "min" なら辞書順最小、"max" なら辞書順最大。
            どちらも、まず辺数が最小の経路だけを対象とする。

    Returns:
        depth:
            最小辺数。到達不能なら -1。
        parent:
            採用した経路における親頂点。始点・到達不能は -1。
        parent_label:
            親から移動した辺のラベル。始点・到達不能は -1。
        visit_order:
            頂点の確定順（始点を含む）。親は常に子より先に現れる。
            各頂点の値を parent から順に計算する際にも使える。

    計算量:
        O(N + M log(M+1)) 時間、O(N + M) 追加空間。
        辺ラベルが固定の小さい整数範囲ならバケット化して高速化可能。

    Note:
        辞書順だけでなく、最短辺数を必ず最優先する。
        辞書順BFS (LexBFS) と呼ばれる別の頂点順序アルゴリズムとは異なる。
    """
    n = len(graph)
    if not 0 <= start < n:
        raise ValueError("start is out of range")
    if order not in ("min", "max"):
        raise ValueError('order must be "min" or "max"')

    depth = [-1] * n
    parent = [-1] * n
    parent_label = [-1] * n
    depth[start] = 0
    visit_order = [start]

    # 同じ長さ・同じラベル列で到達する頂点を一括処理する。
    queue = deque([([start], 0)])

    while queue:
        vertices, d = queue.popleft()
        buckets: dict[int, list[tuple[int, int]]] = {}

        # まずグループ全体の遷移を集め、親の処理順で
        # ラベルの優先順位が崩れないようにする。
        for v in vertices:
            for to, label in graph[v]:
                if depth[to] == -1:
                    buckets.setdefault(label, []).append((v, to))

        for label in sorted(buckets, reverse=(order == "max")):
            next_vertices = []
            for v, to in buckets[label]:
                if depth[to] != -1:
                    continue
                depth[to] = d + 1
                parent[to] = v
                parent_label[to] = label
                next_vertices.append(to)
                visit_order.append(to)

            if next_vertices:
                queue.append((next_vertices, d + 1))

    return depth, parent, parent_label, visit_order


def restoreLexicographicPath(
    parent: list[int], goal: int
) -> list[int]:
    """parent 配列から始点 -> goal の頂点列を復元する。

    到達不能と始点を区別したい場合は、別途 depth を確認すること。
    """
    path = []
    while goal != -1:
        path.append(goal)
        goal = parent[goal]
    return path[::-1]
