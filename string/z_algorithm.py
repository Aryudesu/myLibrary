class ZAlgo:
    """
    Z-Algorithmライブラリ
    Edited by Aryu
    """
    def __init__(self, S: str):
        self.N = len(S)
        if self.N == 0:
            self.data = []
            return
        self.data = [0] * self.N
        self.data[0] = self.N
        i = 1
        j = 0
        while i < self.N:
            while i + j < self.N and S[j] == S[i+j]:
                j += 1
            self.data[i] = j
            if j == 0:
                i += 1
                continue
            k = 1
            while i + k < self.N and k + self.data[k] < j:
                self.data[i + k] = self.data[k]
                k += 1
            i += k
            j -= k

    def get(self):
        """結果を取得します"""
        return self.data
    
    @staticmethod
    def findAll(text: str, pattern: str) -> list[int]:
        """text中にpatternが出現する開始位置を返却する"""
        if not pattern:
            return list(range(text) + 1)
        joinData = pattern + "#" + text
        za = ZAlgo(joinData)
        m = len(pattern)
        res = []
        for i in range(m + 1, len(joinData)):
            if za[i] >= m:
                res.append(i-m-1)
        return res

    def lcp_with_prefix(self, i:int)-> int:
        """S[i:]とS自体の最長共通連続部分列を取得する"""
        return self.data[i]

    def __getitem__(self, idx: int)-> int:
        """Z[i]を取得可能にする"""
        return self.data[idx]

    def __len__(self):
        """元の文字列の長さを取得"""
        return self.N

# === ABC141E
N = int(input())
S = input()
res = 0
for i in range(N):
    za = ZAlgo(S[i:])
    for j in range(len(za)):
        l = min(za[j], j)
        res = max(res, l)
print(res)
