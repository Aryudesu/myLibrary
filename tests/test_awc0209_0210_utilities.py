import itertools
import random
import unittest

from dp.adjacentSelectionDP import AdjacentSelectionDP
from dp.moduloSelectionDP import ModuloSelectionDP
from algorithm.circularWeightedDistance import circularWeightedDistance
from algorithm.atLeastKSelection import AtLeastKSelection
from graph.functionalGraph.functionalGraph import FunctionalGraph
from graph.treeKDominatingSet import TreeKDominatingSet


class TestUtilities(unittest.TestCase):
    def test_dp(self):
        rng = random.Random(209)
        for _ in range(100):
            n = rng.randrange(1,7)
            m = rng.randrange(1,8)
            choices = [[rng.randrange(-3,4) for _ in range(2)] for _ in range(n)]
            a = AdjacentSelectionDP(n, mod=7)
            b = ModuloSelectionDP(m, mod=7)
            for row in choices:
                a.step(row)
                b.step(row)
            paths = list(itertools.product(*choices))
            for k in range(n+1):
                self.assertEqual(a.get(k),sum(sum(x==y for x,y in zip(p,p[1:]))==k for p in paths)%7)
            for x in range(m):
                self.assertEqual(b.get(x),sum(sum(p)%m==x for p in paths)%7)

    def test_graph_and_cycle(self):
        rng = random.Random(210)
        for n in range(1,15):
            for _ in range(20):
                p = [rng.randrange(n) for _ in range(n)]
                w = [rng.randrange(-5,6) for _ in range(n)]
                fg = FunctionalGraph(p)
                cnt,cost = fg.aggregate(w)
                for v in range(n):
                    nodes = []
                    for u in range(n):
                        x,d = u,0
                        while x != v and not fg.in_cycle[x]:
                            x = p[x]
                            d += 1
                        if x == v:
                            nodes.append((u,d))
                    self.assertEqual(cnt[v],sum(w[u] for u,d in nodes))
                    self.assertEqual(cost[v],sum(w[u]*d for u,d in nodes))
                for cycle in fg.cycles:
                    W = [cnt[v] for v in cycle]
                    L = len(W)
                    self.assertEqual(circularWeightedDistance(W),[sum(w*((i-j)%L) for j,w in enumerate(W)) for i in range(L)])

    def test_selection_and_tree(self):
        rng = random.Random(211)
        for n in range(1,9):
            for _ in range(25):
                pairs = [(rng.randrange(-5,6),rng.randrange(-5,6)) for _ in range(n)]
                s = AtLeastKSelection(pairs)
                masks = list(itertools.product(range(2),repeat=n))
                for k in range(n+1):
                    exact = min(sum(p[c] for p,c in zip(pairs,mask)) for mask in masks if sum(mask)==k)
                    atleast = min(sum(p[c] for p,c in zip(pairs,mask)) for mask in masks if sum(mask)>=k)
                    self.assertEqual(s.getMinCostExactly(k),exact)
                    self.assertEqual(s.getMinCostAtLeast(k),atleast)
                    self.assertEqual(s.solveAtLeast(pairs,k),atleast)
                g = [[] for _ in range(n)]
                for v in range(1,n):
                    u = rng.randrange(v)
                    g[v].append(u)
                    g[u].append(v)
                A = [p[0] for p in pairs]
                K = [rng.randrange(4) for _ in range(n)]
                ans = min(sum(a*c for a,c in zip(A,mask)) for mask in masks
                          if all(mask[v] or sum(mask[u] for u in g[v])>=K[v] for v in range(n)))
                self.assertEqual(TreeKDominatingSet(g,A,K).solve(),ans)
                self.assertEqual(TreeKDominatingSet(g,A,K).solve(n-1),ans)

    def test_edges(self):
        self.assertEqual(AdjacentSelectionDP(0).get(0),1)
        a = AdjacentSelectionDP(0)
        a.step([])
        a.step([1])
        self.assertEqual(a.get(0),0)
        b = ModuloSelectionDP(1)
        b.step([0,0])
        self.assertEqual(b.get(0),2)
        self.assertEqual(circularWeightedDistance([]),[])
        self.assertEqual(AtLeastKSelection().getMinCostAtLeast(1),float("inf"))
        self.assertEqual(TreeKDominatingSet([[]],[0]).solve(),0)


if __name__ == "__main__":
    unittest.main()
