from heapq import heappop, heappush

INF = 10**18


class ImportantNodeDistances:
    """
    重要頂点を圧縮し、重要頂点間の最短距離を管理するクラス。

    頂点番号・圧縮IDはともに0-indexed。
    有向グラフにも対応。
    """

    def __init__(
        self,
        graph: list[list[tuple[int, int]]],
        nodes: list[int],
    ):
        self.graph = graph

        # 順序を保ちながら重複除去
        self.nodes = list(dict.fromkeys(nodes))
        self.size = len(self.nodes)

        self.node_to_id = {
            node: node_id
            for node_id, node in enumerate(self.nodes)
        }

        self.dist = self._build_distances()

    def __len__(self) -> int:
        return self.size

    def __contains__(self, node: int) -> bool:
        """元グラフ上の頂点が重要頂点に含まれるか判定します。"""
        return node in self.node_to_id

    def get_id(self, node: int) -> int:
        """元グラフ上の頂点番号から圧縮IDを取得します。"""
        if node not in self.node_to_id:
            raise KeyError(f"{node} is not an important node")
        return self.node_to_id[node]

    def get_node(self, node_id: int) -> int:
        """圧縮IDから元グラフ上の頂点番号を取得します。"""
        if not 0 <= node_id < self.size:
            raise IndexError("important node ID out of range")
        return self.nodes[node_id]

    def get_distance_by_id(self, src_id: int, dst_id: int) -> int:
        """圧縮IDを指定して最短距離を取得します。"""
        return self.dist[src_id][dst_id]

    def get_distance(self, src: int, dst: int) -> int:
        """元グラフ上の頂点番号を指定して最短距離を取得します。"""
        return self.dist[self.get_id(src)][self.get_id(dst)]

    def is_reachable_by_id(self, src_id: int, dst_id: int) -> bool:
        """圧縮IDを指定して到達可能性を判定します。"""
        return self.dist[src_id][dst_id] < INF

    def is_reachable(self, src: int, dst: int) -> bool:
        """元グラフ上の頂点番号を指定して到達可能性を判定します。"""
        return self.get_distance(src, dst) < INF

    def _dijkstra(self, start: int) -> list[int]:
        n = len(self.graph)
        dist = [INF] * n
        dist[start] = 0

        heap = [(0, start)]

        while heap:
            current_dist, node = heappop(heap)

            if current_dist != dist[node]:
                continue

            for next_node, weight in self.graph[node]:
                next_dist = current_dist + weight

                if next_dist < dist[next_node]:
                    dist[next_node] = next_dist
                    heappush(heap, (next_dist, next_node))

        return dist

    def _build_distances(self) -> list[list[int]]:
        distances = [[INF] * self.size for _ in range(self.size)]

        for src_id, src in enumerate(self.nodes):
            dist = self._dijkstra(src)

            for dst_id, dst in enumerate(self.nodes):
                distances[src_id][dst_id] = dist[dst]

        return distances
