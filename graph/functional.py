from typing import Tuple

class FunctionalGraph:
    """list[int]形式のグラフについてのUtility"""
    def __init__(self, graph: list[int]):
        self.graph = graph.copy()
        self.N = len(graph)

    def getCycle(self, node: int, memo: set[int], result: list[int])->int:
        """nodeから開始し，サイクルを取得します"""
        if node in memo:
            result.append(node)
            return node
        nextNode = self.graph[node]
        memo.add(node)
        res = self.getCycle(nextNode, memo, result)
        if res == node:
            return -1
        if res >= 0:
            result.append(node)
        return res

    def getCycles(self)-> list[list[int]]:
        """サイクルを取得します"""
        memo = set()
        result = []
        for n in range(self.N):
            if n in memo:
                continue
            res = []
            self.getCycle(n, memo, res)
            result.append(res)
        return result

def dfs(node, M, mTimesMemo)->bool:
    s1, s2 = node//M, node%M
    s3 = (A * s2 + B * s1) % M
    nextNode = s2 * M + s3
    if s1 == 0 or s2 == 0:
        mTimesMemo[node] = True
        return True
    if mTimesMemo[node] is None:
        res = dfs(nextNode, M, mTimesMemo)
        mTimesMemo[node] = res
    return mTimesMemo[node]

def xy2num(x: int, y: int, M: int)-> int:
    return x * M + y

def num2xy(num: int, M: int)-> Tuple[int, int]:
    return (num//M, num%M)

M, A, B = map(int, input().split())
mTimesMemo = [None] * (M * M)
graph = [None] * (M * M)
for i in range(M):
    for j in range(M):
        s1, s2 = i, j
        s3 = (A * s2 + B * s1) % M
        n1 = xy2num(s1, s2, M)
        n2 = xy2num(s2, s3, M)
        # 自己ループのときにn1がMの倍数であればTrue
        if n1 == n2:
            mTimesMemo[n1] = n1 % M == 0
        graph[n1] = n2
fg = FunctionalGraph(graph)
cycle = fg.getCycles()

for dat in cycle:
    f = False
    # 長さが1より大きければループ
    if len(dat) > 1:
        for d in dat:
            s1, s2 = d//M, d%M
            if s1 == 0 or s2 == 0:
                f = True
                break
        for d in dat:
            mTimesMemo[d] = f
partition = None
for n in range(M*M):
    dfs(n, M, mTimesMemo)
print(mTimesMemo.count(False))
