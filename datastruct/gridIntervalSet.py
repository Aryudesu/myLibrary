from sortedcontainers import SortedSet

INF = 10**18

class HalfOpenIntervalSet:
    """
    半開区間 [L, R) の集合を管理する。
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

    def iter_intervals(self):
        """区間列挙用（(L, R) のイテレータ）"""
        return iter(self._seg)

    def __repr__(self):
        return f"HalfOpenIntervalSet({list(self._seg)}, total={self.total})"


class GridIntervalSet:
    """
    整数グリッドの閉区間 [L, R] を管理する版。
    内部では [L, R+1) の半開区間で管理する。
    - total: 覆っているマスの個数
    """

    def __init__(self):
        self._base = HalfOpenIntervalSet()

    def add(self, L: int, R: int) -> int:
        """
        閉区間 [L, R] を追加し、
        「新しく黒くなったマスの数」を返す。
        """
        # [L, R] -> [L, R+1) に変換
        return self._base.add(L, R + 1)

    def contains_point(self, x: int) -> bool:
        """マス x が黒く塗られているか"""
        return self._base.contains_point(x)

    @property
    def total(self) -> int:
        """覆っているマス数"""
        return self._base.total

    def __repr__(self):
        return f"GridIntervalSet(total={self.total}, base={self._base})"
