from collections import defaultdict

class LCS:
    """
    最長共通部分列 (Longest Common Subsequence)
    """

    def __init__(self, S: str, T: str):

        self.S = S
        self.T = T

        self.N = len(S)
        self.M = len(T)

        # dp[i][j]
        # S[i], T[j] を最後に使うLCS長
        self.dp = [[0] * self.M for _ in range(self.N)]

        # 遷移元
        self.prev = [[(-1, -1)] * self.M for _ in range(self.N)]

        self.built = False

    def build(self) -> None:
        """DPデータの構築を行います"""
        S = self.S
        T = self.T

        t_pos = defaultdict(list)
        for j, c in enumerate(T):
            t_pos[c].append(j)
        # 初期化
        for j in t_pos[S[0]]:
            self.dp[0][j] = 1
        # DP
        for i in range(1, self.N):
            best_len = 0
            best_j = -1
            for j in range(self.M):
                # 採用
                if S[i] == T[j]:
                    self.dp[i][j] = best_len + 1
                    self.prev[i][j] = (i - 1, best_j)
                elif self.dp[i - 1][j] > self.dp[i][j]:
                    self.dp[i][j] = self.dp[i - 1][j]
                    self.prev[i][j] = self.prev[i - 1][j]
                # 「jより左」の最大を更新
                if self.dp[i - 1][j] > best_len:
                    best_len = self.dp[i - 1][j]
                    best_j = j
        self.built = True

    def restore(self) -> str:
        """LCSを復元します"""
        if not self.built:
            self.build()
        end_i = self.N - 1
        end_j = max(range(self.M), key=lambda j: self.dp[end_i][j])
        if self.dp[end_i][end_j] == 0:
            return ""
        result = []
        i, j = end_i, end_j
        while j != -1:
            result.append(self.T[j])
            i, j = self.prev[i][j]
        result.reverse()
        return "".join(result)

    def solve(self) -> str:
        """LCSを取得します"""
        return self.restore()

#=== Educational DP Contest/DPまとめコンテスト  F問題
S = input()
T = input()
lcs = LCS(S, T)
print(lcs.solve())
