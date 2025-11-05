class Doubling:
    """
    ダブリングライブラリ
    0～N-1という番号が振られたN個のノードを前提とする
    iからgraph[i]に遷移する場合の移動先計算することに特化
    """
    def __init__(self, graph: list[int], maxPow: int = 30):
        """
        初期化
        graph: グラフ（次の遷移先）
        maxPow: 最大操作ビット数
        """
        self.N = len(graph)
        self.M = maxPow
        self.data = self._makeData(graph)

    def _makeData(self, graph: list[int]) -> list[list[int]]:
        """事前データ作成"""
        result = [[graph[i] for i in range(self.N)]]
        for _ in range(1, self.M):
            result.append([result[-1][result[-1][i]] for i in range(self.N)])
        return result
    
    def jump(self, v: int, t: int) -> int:
        """vからt回操作後にどこにいるかを取得します"""
        res = v
        for i in range(t.bit_length()):
            if t & (1 << i):
                res = self.data[i][res]
        return res

    def step(self, v) -> int:
        """vの次の遷移先を取得します"""
        return self.data[0][v]

    def maxStep(self) -> int:
        """今回の設定で計算可能な最大ステップ数"""
        return 2**self.M - 1

N, Q = map(int, input().split())
A = [int(l) - 1 for l in input().split()]
result = []
db = Doubling(A, (10**9+1).bit_length())
for q in range(Q):
    x, y = map(int, input().split())
    result.append(db.jump(x-1, y) + 1)

for r in result:
    print(r)
