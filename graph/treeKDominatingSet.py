from heapq import nsmallest


class TreeKDominatingSet:
    """非選択頂点 v に少なくとも k[v] 個の選択済み隣接頂点を要求する木DP。
    graph は0-indexedの無向木、Aは整数費用（負数可）。
    kは非負整数または頂点別の配列。非再帰。solve() は最小費用。
    時間 O(N log(min(K,N)+2))（K=max(k)、固定Kなら O(N)）、空間 O(N)。
    """
    def __init__(self, graph, A, k=2):
        self.graph = graph
        self.A = list(A)
        n = len(graph)
        self.k = [k]*n if isinstance(k,int) else list(k)
        if len(self.A) != n or len(self.k) != n or any(x<0 for x in self.k):
            raise ValueError("invalid costs or k")

    def solve(self, root=0):
        g,A,K = self.graph,self.A,self.k
        n = len(g)
        if not n:
            return 0
        if not 0 <= root < n:
            raise IndexError(root)
        parent = [-2]*n
        parent[root] = -1
        order = [root]
        for v in order:
            for u in g[v]:
                if u == parent[v]:
                    continue
                if parent[u] != -2:
                    raise ValueError("graph must be a tree")
                parent[u] = v
                order.append(u)
        if len(order) != n:
            raise ValueError("graph must be connected")
        inf = float("inf")
        w0,w1,b = [inf]*n,[inf]*n,[0]*n
        for v in reversed(order):
            black = A[v]
            white = count = 0
            positive = []
            for u in g[v]:
                if parent[u] != v:
                    continue
                black += min(w1[u],b[u])
                if b[u] <= w0[u]:
                    white += b[u]
                    count += 1
                else:
                    white += w0[u]
                    positive.append(b[u]-w0[u])
            b[v] = black
            need = max(0,K[v]-count)
            if need == 0:
                w0[v] = w1[v] = white
            elif need <= len(positive):
                ds = nsmallest(need,positive)
                extra = sum(ds)
                w0[v] = white + extra
                w1[v] = white + extra - ds[-1]
            elif need == len(positive)+1:
                w1[v] = white + sum(positive)
        return min(w0[root],b[root])
