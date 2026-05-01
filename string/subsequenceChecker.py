class SubsequenceChecker:
    def __init__(self, S: str):
        self.N = len(S)
        self.nxt = [[-1] * 26 for _ in range(self.N + 1)]

        for i in range(self.N - 1, -1, -1):
            self.nxt[i] = self.nxt[i + 1].copy()
            self.nxt[i][ord(S[i]) - ord("a")] = i + 1

    def contains(self, T: str) -> bool:
        """T が S の部分列なら True"""
        pos = 0
        for c in T:
            pos = self.nxt[pos][ord(c) - ord("a")]
            if pos == -1:
                return False
        return True
