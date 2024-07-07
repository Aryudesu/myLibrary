import sys
from collections import deque

sys.setrecursionlimit(10**6)

class Tree:
    """木についてのクラス"""
    def __init__ (self, N = 1):
        self.N = N
        self.graph = dict()

    def set_node(self, a, b, c=1):
        """aからbを繋ぐ重さcのノードを設定します"""
        tmp = self.graph.get(a, [])
        tmp.append((b, c))
        self.graph[a] = tmp

    def longest_node(self, s):
        """指定したパスから最長のパスを取得します"""
        dist = [None] * self.N
        que = deque([s])
        dist[s] = 0
        while que:
            v = que.popleft()
            d = dist[v]
            for w, c in self.graph[v]:
                if dist[w] is not None:
                    continue
                dist[w] = d + c
                que.append(w)
        d = max(dist)
        return dist.index(d), d


# *** Example (ABC361 E) ***
N = int(input())
tree = Tree(N)
AllCost = 0
for n in range(N-1):
    a, b, c = [int(l) for l in input().split()]
    tree.set_node(a - 1, b - 1, c)
    tree.set_node(b - 1, a - 1, c)
    AllCost += c
u, _ = tree.longest_node(0)
v, d = tree.longest_node(u)
print(AllCost * 2 - d)
