class Rerooting:
    """
    全方位木DP（Rerooting）

    各頂点を根としたときのDP値を O(N) で求める。
    再帰を使わないため、深い木でも利用可能。

    Parameters
    ----------
    n : int
        頂点数

    identity : T
        merge の単位元

    merge : (T, T) -> T
        複数の隣接頂点から来るDP値を結合する関数。
        結合則を満たす必要がある。
        可換である必要はない。

    add_vertex : (T, int) -> T
        隣接頂点から来るDP値をすべて結合したあと、
        頂点 v 自身の情報を追加する関数。

    lift : (T, E, int, int) -> T
        src 側で完成したDP値を、辺を越えて dst 側へ渡す関数。

        lift(value, edge_data, src, dst)

    Notes
    -----
    無向辺 u-v に対して、

        add_edge(u, v, data_uv, data_vu)

    とすると、

        u -> v では data_uv
        v -> u では data_vu

    が lift に渡される。

    data_vu を省略した場合は data_uv と同じ値を使用する。
    """

    def __init__(
        self,
        n: int,
        identity,
        merge,
        add_vertex,
        lift,
    ):
        self.n = n
        self.identity = identity
        self.merge = merge
        self.add_vertex = add_vertex
        self.lift = lift

        # graph[v] = [(to, reverse_index, edge_data), ...]
        self.graph = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int, data_uv=None, data_vu=None) -> None:
        """
        無向辺 u-v を追加する。

        data_uv:
            u -> v の向きで使用する辺情報

        data_vu:
            v -> u の向きで使用する辺情報
            省略時は data_uv と同じ
        """
        if data_vu is None:
            data_vu = data_uv

        ui = len(self.graph[u])
        vi = len(self.graph[v])

        self.graph[u].append((v, vi, data_uv))
        self.graph[v].append((u, ui, data_vu))

    def solve(self, root: int = 0):
        """
        各頂点を根としたときのDP値を返す。

        Returns
        -------
        answer : list[T]
            answer[v] は頂点 v を根としたときのDP値
        """
        n = self.n

        if n == 0:
            return []

        graph = self.graph
        merge = self.merge
        add_vertex = self.add_vertex
        lift = self.lift
        identity = self.identity

        parent = [-2] * n
        parent_edge_index = [-1] * n
        order = [root]
        parent[root] = -1

        # 根付き木を構築
        for v in order:
            for i, (to, rev, _) in enumerate(graph[v]):
                if to == parent[v]:
                    continue
                if parent[to] != -2:
                    continue

                parent[to] = v
                parent_edge_index[to] = rev
                order.append(to)

        if len(order) != n:
            raise ValueError("graph must be a connected tree")

        # child_to_parent[v]:
        # 頂点 v 側の部分木から parent[v] へ渡すDP値
        child_to_parent = [identity for _ in range(n)]

        # bottom-up DP
        for v in reversed(order):
            merged = identity

            for to, _, _ in graph[v]:
                if parent[to] == v:
                    merged = merge(merged, child_to_parent[to])

            value = add_vertex(merged, v)

            if parent[v] != -1:
                _, _, edge_data = graph[v][parent_edge_index[v]]

                child_to_parent[v] = lift(
                    value,
                    edge_data,
                    v,
                    parent[v],
                )

        # parent_to_child[v]:
        # parent[v] 側から頂点 v へ渡されるDP値
        parent_to_child = [identity for _ in range(n)]

        answer = [None] * n

        # top-down DP
        for v in order:
            degree = len(graph[v])
            contributions = [identity] * degree

            for i, (to, _, _) in enumerate(graph[v]):
                if to == parent[v]:
                    contributions[i] = parent_to_child[v]
                else:
                    contributions[i] = child_to_parent[to]

            # prefix[i] = contributions[0:i] の結合
            prefix = [identity] * (degree + 1)

            for i in range(degree):
                prefix[i + 1] = merge(
                    prefix[i],
                    contributions[i],
                )

            # suffix[i] = contributions[i:degree] の結合
            suffix = [identity] * (degree + 1)

            for i in range(degree - 1, -1, -1):
                suffix[i] = merge(
                    contributions[i],
                    suffix[i + 1],
                )

            answer[v] = add_vertex(prefix[degree], v)

            # v から各子へDP値を渡す
            for i, (to, _, edge_data) in enumerate(graph[v]):
                if to == parent[v]:
                    continue

                without_to = merge(
                    prefix[i],
                    suffix[i + 1],
                )

                value = add_vertex(without_to, v)

                parent_to_child[to] = lift(
                    value,
                    edge_data,
                    v,
                    to,
                )

        return answer


N = int(input())

edges = []
for _ in range(N - 1):
    a, b = map(int, input().split())
    a -= 1
    b -= 1
    edges.append((a, b))

C = list(map(int, input().split()))


def merge(a, b):
    return (
        a[0] + b[0],
        a[1] + b[1],
    )


def add_vertex(value, v):
    weight_sum, distance_sum = value

    return (
        weight_sum + C[v],
        distance_sum,
    )


def lift(value, edge_data, src, dst):
    weight_sum, distance_sum = value

    return (
        weight_sum,
        distance_sum + weight_sum,
    )


rr = Rerooting(
    n=N,
    identity=(0, 0),
    merge=merge,
    add_vertex=add_vertex,
    lift=lift,
)

for a, b in edges:
    rr.add_edge(a, b)

result = rr.solve()

answer = min(distance_sum for weight_sum, distance_sum in result)

print(answer)
