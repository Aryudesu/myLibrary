from sortedcontainers import SortedSet

INF = 10**18

class HalfOpenIntervalSet:
    """
    半開区間 [L, R)をSortedSetで。
    - 常に互いに重ならない区間のみを保持する。
    - [1,3) と [3,5) みたいに隣接するものはマージして [1,5) にする。
    - total は覆っている長さ（実数区間の長さ的なイメージ）。
    """

    def __init__(self):
        # (L, R) をソートして保持
        self._seg = SortedSet()
        self.total = 0  # 全区間の長さの総和

    def _len_interval(self, L: int, R: int) -> int:
        # 半開区間なので長さは R-L
        return R - L

    def add(self, L: int, R: int) -> int:
        """
        半開区間 [L, R) を追加し、
        「新しく覆われた長さ（すでに covered だった部分を除いた差分）」を返す。
        """
        if R <= L:
            return 0  # 空区間

        seg = self._seg
        newL, newR = L, R

        # L の挿入位置を探す
        idx = seg.bisect_left((L, -INF))

        # 左側の区間が [L, R) と重なる or 隣接するなら、そこからマージ開始
        # （seg[idx-1].R >= L なら [L, R) と接続 or 重なり）
        if idx > 0 and seg[idx - 1][1] >= L:
            idx -= 1

        removed = 0
        start = idx

        # [L, R) と重なる or 隣接する区間をすべてマージ
        while idx < len(seg) and seg[idx][0] <= newR:
            l0, r0 = seg[idx]
            newL = min(newL, l0)
            newR = max(newR, r0)
            removed += self._len_interval(l0, r0)
            idx += 1

        # 古い区間を削除
        for _ in range(idx - start):
            seg.pop(start)

        # 新しいマージ後区間を追加
        seg.add((newL, newR))
        added = self._len_interval(newL, newR)

        delta = added - removed
        self.total += delta
        return delta

    def contains_point(self, x: int) -> bool:
        """x がいずれかの区間 [L, R) に含まれているか (L <= x < R)"""
        seg = self._seg
        idx = seg.bisect_left((x, -INF))

        # 右側の候補
        if idx < len(seg):
            L, R = seg[idx]
            if L <= x < R:
                return True

        # 左側の候補
        if idx > 0:
            L, R = seg[idx - 1]
            if L <= x < R:
                return True

        return False

    def remove(self, L: int, R: int) -> int:
        """
        半開区間 [L, R) を削る。
        戻り値: 実際に「消えた長さ」（= [L,R) ∩ covered の長さ）
        """
        if R <= L:
            return 0

        seg = self._seg
        idx = seg.bisect_left((L, -INF))

        if idx > 0 and seg[idx - 1][1] > L:
            idx -= 1

        removed_total = 0
        added_back = 0
        start = idx
        new_pieces = []

        while idx < len(seg) and seg[idx][0] < R:
            a, b = seg[idx]
            removed_total += (b - a)

            if a < L:
                if b <= R:
                    new_pieces.append((a, L))
                    added_back += (L - a)
                else:
                    new_pieces.append((a, L))
                    new_pieces.append((R, b))
                    added_back += (L - a) + (b - R)
            else:
                if b > R:
                    new_pieces.append((R, b))
                    added_back += (b - R)
                else:
                    pass

            idx += 1

        for _ in range(idx - start):
            seg.pop(start)

        for iv in new_pieces:
            seg.add(iv)

        delta = removed_total - added_back
        self.total -= delta
        return delta

    def iter_intervals(self):
        """区間列挙用（(L, R) のイテレータ）"""
        return iter(self._seg)

    def __repr__(self):
        return f"HalfOpenIntervalSet({list(self._seg)}, total={self.total})"
