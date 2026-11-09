from typing import Iterable, Iterator


class XorBasis:
    """
    非負整数の XOR 線形基底（部分集合 XOR）。

    - add(x): 要素を追加。ランクが増えたとき True
    - can_make(x): 部分集合 XOR で x を作れるか
    - max_xor(x=0), min_xor(x=0): x XOR y の最大/最小値
    - count_distinct(): 作れる異なる XOR 値の個数
    - count_ways(x): XOR が x になる部分集合の個数
    - enumerate_xors(): 作れる異なる XOR 値を一度ずつ列挙
    - merge(other): 2 つの元の要素集合を合わせた新しい基底

    計算量: add/can_make/max_xor/min_xor は O(bit_width)、
            enumerate_xors は O(2^rank)。
    count_ways のため、線形従属なものも含めた追加要素数 n を保持する。
    """

    def __init__(self, values: Iterable[int] = (), bit_width: int = 60):
        if bit_width <= 0:
            raise ValueError("bit_width must be positive")
        self.bit_width = bit_width
        self.basis = [0] * bit_width
        self.rank = 0
        self.n = 0

        for x in values:
            self.add(x)

    def add(self, x: int) -> bool:
        """x を追加し、ランクが増えた場合 True を返す。"""
        if x < 0 or x.bit_length() > self.bit_width:
            raise ValueError("x is out of range")

        self.n += 1
        for i in range(self.bit_width - 1, -1, -1):
            if not ((x >> i) & 1):
                continue
            if self.basis[i]:
                x ^= self.basis[i]
            else:
                self.basis[i] = x
                self.rank += 1
                return True
        return False

    def can_make(self, x: int) -> bool:
        """元の要素の部分集合 XOR で x を作れるか。"""
        if x < 0 or x.bit_length() > self.bit_width:
            return False

        for i in range(self.bit_width - 1, -1, -1):
            if (x >> i) & 1:
                if not self.basis[i]:
                    return False
                x ^= self.basis[i]
        return x == 0

    def max_xor(self, x: int = 0) -> int:
        """基底から作れる y に対して x XOR y を最大化する。"""
        if x < 0:
            raise ValueError("x must be nonnegative")
        for v in reversed(self.basis):
            if v and (x ^ v) > x:
                x ^= v
        return x

    def min_xor(self, x: int = 0) -> int:
        """基底から作れる y に対して x XOR y を最小化する。"""
        if x < 0:
            raise ValueError("x must be nonnegative")
        for v in reversed(self.basis):
            if v and (x ^ v) < x:
                x ^= v
        return x

    def count_distinct(self) -> int:
        """作れる異なる XOR 値の個数（2^rank）。"""
        return 1 << self.rank

    def count_ways(self, x: int) -> int:
        """XOR が x になる元の要素の部分集合数（空集合を含む）。"""
        return (1 << (self.n - self.rank)) if self.can_make(x) else 0

    def enumerate_xors(self) -> Iterator[int]:
        """異なる部分集合 XOR 値をすべて列挙する（数値順ではない）。"""
        values = [v for v in self.basis if v]
        current = 0
        yield current

        # 反射 Gray code に沿って、隣の値との差分だけ XOR する。
        for mask in range(1, 1 << self.rank):
            i = (mask & -mask).bit_length() - 1
            current ^= values[i]
            yield current

    def merge(self, other: "XorBasis") -> "XorBasis":
        """元の要素集合を結合した新しい基底を返す（元の基底は変更しない）。"""
        if self.bit_width != other.bit_width:
            raise ValueError("bit_width mismatch")

        result = XorBasis(bit_width=self.bit_width)
        for v in self.basis:
            if v:
                result.add(v)
        for v in other.basis:
            if v:
                result.add(v)

        # 基底だけでは従属な元の要素数が失われるため復元する。
        result.n = self.n + other.n
        return result
