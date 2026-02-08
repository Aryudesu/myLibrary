from dataclasses import dataclass
from typing import Iterator, Tuple
from atcoder.dsu import DSU


@dataclass
class KruskalData:
    """クラスカル法で返却されるデータ"""
    nodeA: int
    nodeB: int
    cost: int
    newLeader: int

class Kruskal:
    @staticmethod
    def kruskal(n: int, edges: list[Tuple[int, int, int]])-> Iterator[KruskalData]:
        """
        クラスカル法
        @param n: ノード数
        @param edges: (コスト, ノードA, ノードB)を要素とする配列
        """
        edges = sorted(edges)
        dsu = DSU(n)
        for c, a, b in edges:
            if dsu.same(a, b):
                continue
            dsu.merge(a, b)
            yield KruskalData(a, b, c, dsu.leader(a))
    
    @staticmethod
    def kruskal_mst(n: int, edges: list[Tuple[int, int, int]])->int:
        """最小全域木のコストの総和"""
        return sum([data.cost for data in Kruskal.kruskal(n, edges)])

# 競技プログラミングの鉄則A67
N, M = map(int, input().split())
edges = []
for _ in range(M):
    a, b, c = map(int, input().split())
    edges.append((c, a-1, b-1))
print(Kruskal.kruskal_mst(N, edges))
