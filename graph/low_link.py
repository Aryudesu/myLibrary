from collections import defaultdict


class LowLink:
    def __init__(self, graph: dict):
        self.graph = graph
        self.ord = {}
        self.low = {}
        self.parent = {}
        self.bridges = []
        self.articulation_points = set()
        self._time = 0

        for v in graph:
            if v not in self.ord:
                self.parent[v] = None
                self._dfs(v)

    def _dfs(self, v):
        self.ord[v] = self.low[v] = self._time
        self._time += 1
        child_count = 0
        is_articulation = False

        for to in self.graph[v]:
            if to == self.parent.get(v):
                continue
            if to in self.ord:
                self.low[v] = min(self.low[v], self.ord[to])
            else:
                self.parent[to] = v
                child_count += 1
                self._dfs(to)
                self.low[v] = min(self.low[v], self.low[to])
                if self.low[to] > self.ord[v]:
                    self.bridges.append((v, to))
                if self.parent[v] is None:
                    if child_count > 1:
                        self.articulation_points.add(v)
                else:
                    if self.low[to] >= self.ord[v]:
                        is_articulation = True

        if is_articulation:
            self.articulation_points.add(v)


graph = defaultdict(set)
graph[1].update([2, 3])
graph[2].update([1, 3, 4])
graph[3].update([1, 2, 4])
graph[4].update([2, 3, 5])
graph[5].update([4])

low_link = LowLink(graph)
print("Bridges:", low_link.bridges)
print("Articulation Points:", low_link.articulation_points)
