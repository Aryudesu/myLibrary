from collections import deque


class Graph:
    def __init__(self, N):
        self.N = N
        self.graph = [[] for _ in range(N)]
        self.indegree = [0] * N

    def add_edge(self, a, b):
        """辺の追加"""
        self.graph[a].append(b)
        self.indegree[b] += 1

    def sort(self):
        """
        トポロジカルソート
        戻り値は result[頂点番号] = 何番目か
        """
        queue = deque()
        for i in range(self.N):
            if self.indegree[i] == 0:
                queue.append(i)
        topo_order = []
        while queue:
            if len(queue) > 1:
                return None
            current = queue.popleft()
            topo_order.append(current)
            for neighbor in self.graph[current]:
                self.indegree[neighbor] -= 1
                if self.indegree[neighbor] == 0:
                    queue.append(neighbor)
        if len(topo_order) != self.N:
            return []
        return topo_order


# === ABC291E

N, M = [int(l) for l in input().split()]
graph = Graph(N)
for _ in range(M):
    x, y = [int(l) - 1 for l in input().split()]
    graph.add_edge(x, y)

topo_order = graph.sort()
if topo_order:
    result_arr = [0] * N
    for i in range(N):
        result_arr[topo_order[i]] = i + 1
    print("Yes")
    print(*result_arr)
else:
    print("No")
