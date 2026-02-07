from typing import Any


class ModBit:
    """ACLのフェニ木をmod対応したもの"""
    def __init__(self, n: int = 0, mod: int = 998244353) -> None:
        self._n = n
        self._mod = mod
        self.data = [0] * n

    def add(self, p: int, x: Any) -> None:
        assert 0 <= p < self._n
        p += 1
        while p <= self._n:
            self.data[p - 1] = (self.data[p - 1] + x) % self._mod
            p += p & -p

    def sum(self, left: int, right: int) -> Any:
        assert 0 <= left <= right <= self._n
        return (self._sum(right) - self._sum(left)) % self._mod

    def _sum(self, r: int) -> Any:
        result = 0
        while r > 0:
            result = (result + self.data[r - 1]) % self._mod
            r -= r & -r
        return result
