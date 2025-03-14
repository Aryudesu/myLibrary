from collections import defaultdict

inf = 10**18


class Graph:
    def __init__(self):
        self.graph = defaultdict(lambda: [])
        self.node = set()

    def __len__(self):
        return len(self.node)

    def add_edge(self, src, dst, weight):
        self.graph[src].append((dst, weight))
        self.node.add(src)
        self.node.add(dst)

    def get_nodes(self):
        return self.node

    def get_edge(self, node):
        return self.graph[node]


class BellmanFord:
    def __init__(self, graph: Graph, start):
        res = defaultdict(lambda: inf)
        res[start] = 0
        nodes = graph.get_nodes()
        for _ in range(len(graph) - 1):
            for v in nodes:
                for d, w in graph.get_edge(v):
                    if res[v] != inf and res[v] + w < res[d]:
                        res[d] = res[v] + w
        cycle = False
        for v in nodes:
            for d, w in graph.get_edge(v):
                if res[v] + w < res[d]:
                    cycle = True
                    break
            if cycle:
                break
        self.result = None if cycle else res

    def is_contain_ng_dist(self):
        return self.result is None

    def get_result(self):
        return self.result

    def get_distance(self, goal):
        if self.result is None:
            return None
        return self.result[goal]


graph = Graph()
# 負サイクルなし
# graph.add_edge(0, 1, 4)
# graph.add_edge(0, 2, 3)
# graph.add_edge(1, 2, -2)
# graph.add_edge(1, 3, 1)
# graph.add_edge(2, 3, 2)
# 負サイクルあり
graph.add_edge(0, 1, -1)
graph.add_edge(1, 2, -1)
graph.add_edge(2, 0, -1)
graph.add_edge(2, 3, 1)
bf = BellmanFord(graph, 0)
print(bf.is_contain_ng_dist())
print(bf.get_result())
