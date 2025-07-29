from bisect import bisect_left
from typing import List

class LISolver:
    """最長増加部分列の取得"""
    def __init__(self, A: List[int]) -> None:
        """初期化"""
        self.A = A
        self.N = len(A)
        self._length = 0
        self._subseq = []
        self._solved = False

    def _solve(self) -> None:
        """LIS復元"""
        A = self.A
        N = self.N
        INF = float('inf')

        dp_val = []       # 長さiの増加列の末尾最小値
        dp_index = []     # それに対応するAのインデックス
        pos = [0]*N       # A[i]が何番目の位置に入ったか
        prev = [-1]*N     # 復元のための前インデックス

        for i, a in enumerate(A):
            idx = bisect_left(dp_val, a)
            if idx == len(dp_val):
                dp_val.append(a)
                dp_index.append(i)
            else:
                dp_val[idx] = a
                dp_index[idx] = i
            pos[i] = idx
            if idx > 0:
                prev[i] = dp_index[idx - 1]

        # 復元
        length = len(dp_val)
        cur = -1
        for i in range(N - 1, -1, -1):
            if pos[i] == length - 1:
                cur = i
                break

        subseq = []
        while cur != -1:
            subseq.append(A[cur])
            cur = prev[cur]
        subseq.reverse()

        self._length = length
        self._subseq = subseq
        self._solved = True

    def length(self) -> int:
        """最長増加部分列の長さを返す"""
        if not self._solved:
            self._solve()
        return self._length

    def restore(self) -> List[int]:
        """最長増加部分列の具体的な列を返す"""
        if not self._solved:
            self._solve()
        return self._subseq[:]
