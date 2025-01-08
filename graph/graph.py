class Graph:
    def __init__(self, N):
        self.N = N
        self.graph = dict()

    def add_edge(self, a, b):
        """辺の追加"""
        assert a < self.N
        assert b < self.N
        tmp = self.graph.get(a, [])
        tmp.append(b)
        self.graph[a] = tmp
        tmp = self.graph.get(b, [])
        tmp.append(a)
        self.graph[b] = tmp

    def get_edge(self, a):
        """辺の取得"""
        assert a < self.N
        return self.graph.get(a, [])

    def isNibuGraph(self):
        """二分グラフかの判定"""
        data = dict()
        nums = set([i for i in range(self.N)])
        while nums:
            d = nums.pop()
            data[d] = 1
            nodes = set([d])
            while nodes:
                new_nodes = set()
                for n in nodes:
                    for e in self.get_edge(n):
                        if e in nums:
                            data[e] = 1 - data[n]
                            new_nodes.add(e)
                            nums.discard(e)
                nodes = new_nodes
        for n in range(self.N):
            for e in self.get_edge(n):
                if data.get(e) == data.get(n):
                    return False
        return True

N, M = [int(l) for l in input().split()]
graph = Graph(N)
for m in range(M):
    a, b = [int(l) - 1 for l in input().split()]
    graph.add_edge(a, b)
print("Yes" if graph.isNibuGraph() else "No")

