from typing import Sequence


class TSPBitDP:
    """
    全頂点をちょうど1回ずつ訪問する最小コストをBitDPで求める。
    頂点は 0-indexed。距離行列は有向・非対称でもよい。

    dist[i][j]: 頂点iから頂点jへの移動コスト
    solve(start_cost, end_cost=None):
        仮想始点から全頂点を巡る最小コストを返す。
        start_cost[i]: 始点から最初の訪問先iへのコスト
        end_cost[i]: 最後の訪問先iから終点へのコスト
                     Noneなら最後の頂点で終了する。

    計算量: 時間 O(N^2 * 2^N)、空間 O(N * 2^N)
    N=0の場合は0を返す（始点と終点間の移動は考慮しない）。
    """

    def __init__(self, dist: Sequence[Sequence[int]]):
        self.dist = [list(row) for row in dist]
        self.n = len(self.dist)
        if any(len(row) != self.n for row in self.dist):
            raise ValueError("dist must be a square matrix")

    def solve(
        self,
        start_cost: Sequence[int],
        end_cost: Sequence[int] | None = None,
    ) -> int:
        n = self.n
        if len(start_cost) != n:
            raise ValueError("start_cost length must equal n")
        if end_cost is not None and len(end_cost) != n:
            raise ValueError("end_cost length must equal n")
        if n == 0:
            return 0

        size = 1 << n
        goal = size - 1
        # Noneは未到達状態。コストの上限を決める必要がない。
        dp: list[list[int | None]] = [[None] * n for _ in range(size)]
        for i in range(n):
            dp[1 << i][i] = start_cost[i]

        for mask in range(1, size):
            remaining_bits = goal ^ mask
            for now in range(n):
                cost = dp[mask][now]
                if cost is None:
                    continue

                remain = remaining_bits
                while remain:
                    bit = remain & -remain
                    remain ^= bit
                    nxt = bit.bit_length() - 1
                    new_mask = mask | bit
                    new_cost = cost + self.dist[now][nxt]
                    old_cost = dp[new_mask][nxt]
                    if old_cost is None or new_cost < old_cost:
                        dp[new_mask][nxt] = new_cost

        if end_cost is None:
            return min(dp[goal])

        return min(
            dp[goal][i] + end_cost[i]
            for i in range(n)
        )
