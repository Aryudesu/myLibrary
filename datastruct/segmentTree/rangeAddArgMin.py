from typing import Tuple

class RangeAddArgMin:
    """
    区間加算 + 全体最小値 + 最左argmin

    初期値: 全要素 0
    range_add(l, r, x): [l, r) に x 加算
    min(): 全体最小値
    argmin(): 最小値を取る最左index
    min_with_arg(): (最小値, 最左index)
    """

    INF = 10**30

    def __init__(self, n: int):
        self.n = n
        self.size = 1
        while self.size < n:
            self.size <<= 1

        self.min_val = [self.INF] * (2 * self.size)
        self.arg = [self.INF] * (2 * self.size)
        self.lazy = [0] * (2 * self.size)

        for i in range(n):
            self.min_val[self.size + i] = 0
            self.arg[self.size + i] = i

        for i in range(self.size - 1, 0, -1):
            self._pull(i)

    def _pull(self, k: int) -> None:
        l = k << 1
        r = l | 1

        if self.min_val[l] <= self.min_val[r]:
            self.min_val[k] = self.min_val[l]
            self.arg[k] = self.arg[l]
        else:
            self.min_val[k] = self.min_val[r]
            self.arg[k] = self.arg[r]

    def _apply(self, k: int, x: int) -> None:
        self.min_val[k] += x
        self.lazy[k] += x

    def _push(self, k: int) -> None:
        if self.lazy[k] != 0:
            x = self.lazy[k]
            self._apply(k << 1, x)
            self._apply(k << 1 | 1, x)
            self.lazy[k] = 0

    def range_add(self, l: int, r: int, x: int) -> None:
        """[l, r) に x 加算"""
        if l >= r:
            return
        self._range_add(l, r, x, 1, 0, self.size)

    def _range_add(self, l: int, r: int, x: int, k: int, nl: int, nr: int) -> None:
        if nr <= l or r <= nl:
            return

        if l <= nl and nr <= r:
            self._apply(k, x)
            return

        self._push(k)
        mid = (nl + nr) >> 1
        self._range_add(l, r, x, k << 1, nl, mid)
        self._range_add(l, r, x, k << 1 | 1, mid, nr)
        self._pull(k)

    def min(self) -> int:
        return self.min_val[1]

    def argmin(self) -> int:
        return self.arg[1]

    def min_with_arg(self) -> tuple[int, int]:
        return self.min_val[1], self.arg[1]

# === AWC0107
def calcLR(l: int, r: int, T: int, D: int)->Tuple[int, int]:
    return max(0, r - D), min(l, T - D)

T, N, D, Q = map(int, input().split())
sg = RangeAddArgMin(T-D+1)
LR = []
for n in range(N):
    l, r = map(int, input().split())
    LR.append((l, r))
    sl, sr = calcLR(l, r, T, D)
    if sl <= sr:
        sg.range_add(sl, sr + 1, 1)

result = []
for _ in range(Q):
    query = list(map(int, input().split()))
    match query[0]:
        case 1:
            _, i, l, r = query
            i -= 1
            pl, pr = LR[i]
            sl, sr = calcLR(pl, pr, T, D)
            if sl <= sr:
                sg.range_add(sl, sr + 1, -1)
            sl, sr = calcLR(l, r, T, D)
            if sl <= sr:
                sg.range_add(sl, sr + 1, 1)
            LR[i] = (l, r)
        case 2:
            result.append(sg.min_with_arg())
        case _:
            raise ValueError()
for mn, s in result:
    print(s, mn)
