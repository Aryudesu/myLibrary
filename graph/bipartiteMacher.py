class BipartiteMatcher:
    """左側: 0..n_left-1, 右側: 0..n_right-1 の二部グラフ"""
    def __init__(self, n_left: int, n_right: int):
        self.n_left = n_left
        self.n_right = n_right
        self.g = [[] for _ in range(n_left)]
        self.matchR = [-1] * n_right  # 右側 → 対応する左側

    def add_edge(self, l: int, r: int):
        """左 l と 右 r の間に辺を張る"""
        self.g[l].append(r)

    def max_matching(self) -> int:
        """最大マッチングのサイズを返す"""
        result = 0
        def dfs(v: int, memo: list[bool]) -> bool:
            for u in self.g[v]:
                if memo[u]:
                    continue
                memo[u] = True
                if self.matchR[u] == -1 or dfs(self.matchR[u], memo):
                    self.matchR[u] = v
                    return True
            return False
        for v in range(self.n_left):
            memo = [False] * self.n_right
            if dfs(v, memo):
                result += 1
        return result


