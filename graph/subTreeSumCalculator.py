from atcoder.fenwicktree import FenwickTree
import sys
# import pypyjit
sys.setrecursionlimit(10**6)
# pypyjit.set_param('max_unroll_recursion=-1')

class SubTreeSumCalculator:
    """木に対し、頂点重みの部分木和を管理する"""

    def __init__(self, N: int, graph: list[list[int]], root: int=1):
        """初期化．グラフはニ字配列形式．根は何も設定しなければ1をとる．"""
        self.N = N
        self.root = root
        self.graph = graph
        self.inTime = [-1] * (N + 1)
        self.childSize = [0] * (N + 1)
        self.parent = [-1] * (N + 1)
        self.time = 0
        self.ft = FenwickTree(N)
        self._dfs(self.root, -1)

    def _dfs(self, node: int, parent: int):
        self.parent[node] = parent
        self.inTime[node] = self.time
        self.time += 1
        self.childSize[node] = 1
        for nextNode in self.graph[node]:
            if nextNode == parent:
                continue
            self._dfs(nextNode, node)
            self.childSize[node] += self.childSize[nextNode]
    
    def initialize(self, value: int|list[int]):
        """値を初期化します．配列での引数の場合は1-indexedのノード番号に対応します．"""
        if isinstance(value, int):
            if value == 0:
                return
            for i in range(self.N):
                self.ft.add(i, value)
        else:
            assert len(value) == self.N + 1
            for i in range(1, self.N+1):
                self.ft.add(self.inTime[i], value[i])
    
    def getParent(self, p: int)-> int:
        """ノードに対する親の取得"""
        return self.parent[p]
    
    def add(self, p: int, x: int):
        """ノードに値を加算する"""
        self.ft.add(self.inTime[p], x)
    
    def sum(self, root: int)->int:
        """root を根とする部分木の重み総和を取得する"""
        return self.ft.sum(self.inTime[root], self.inTime[root] + self.childSize[root])
    
    def __repr__(self):
        return f"inTime:    {str(self.inTime)}\nchildSize: {str(self.childSize)}\nparent:    {str(self.parent)}"


# === ABC406F
N = int(input())
graph = [[] for _ in range(N+1)]
edge = [(-1, -1)]
for _ in range(N-1):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)
    edge.append((u, v))
ssc = SubTreeSumCalculator(N, graph)
ssc.initialize(1)
allWeight = N
result = []
Q = int(input())
for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 1:
        n, x, w = query
        allWeight += w
        ssc.add(x, w)
    elif query[0] == 2:
        n, y = query
        u, v = edge[y]
        child = v if ssc.getParent(v) == u else u
        a = ssc.sum(child)
        b = allWeight - a
        result.append(abs(a-b))
    else:
        raise Exception()

for r in result:
    print(r)
