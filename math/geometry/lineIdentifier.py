from math import gcd
from typing import Tuple

Point = Tuple[int, int]
Line = Tuple[int, int, int]


class LineIdentifier:
    """直線 ax + by + c = 0 を正規化した (a, b, c) で表す。"""

    @staticmethod
    def normalize(a: int, b: int, c: int) -> Line:
        """直線の係数を既約化し、符号を統一します。"""
        if a == 0 and b == 0:
            raise ValueError("a と b を同時に 0 にはできません")

        g = gcd(gcd(abs(a), abs(b)), abs(c))
        a //= g
        b //= g
        c //= g

        if a < 0 or (a == 0 and b < 0):
            a = -a
            b = -b
            c = -c

        return a, b, c

    @staticmethod
    def from_points(p1: Point, p2: Point) -> Line:
        """異なる2点を通る直線を返します。"""
        if p1 == p2:
            raise ValueError("異なる2点を指定してください")

        x1, y1 = p1
        x2, y2 = p2

        dx = x2 - x1
        dy = y2 - y1

        a = dy
        b = -dx
        c = dx * y1 - dy * x1

        return LineIdentifier.normalize(a, b, c)

    @staticmethod
    def perpendicular_bisector(p1: Point, p2: Point) -> Line:
        """異なる2点を端点とする線分の垂直二等分線を返します。"""
        if p1 == p2:
            raise ValueError("異なる2点を指定してください")

        x1, y1 = p1
        x2, y2 = p2

        dx = x1 - x2
        dy = y1 - y2
        sx = x1 + x2
        sy = y1 + y2

        a = 2 * dx
        b = 2 * dy
        c = -(dx * sx + dy * sy)

        return LineIdentifier.normalize(a, b, c)

    @staticmethod
    def is_parallel(line1: Line, line2: Line) -> bool:
        """2直線が平行または一致しているか判定します。"""
        a1, b1, _ = line1
        a2, b2, _ = line2
        return a1 * b2 == a2 * b1

    @staticmethod
    def is_same(line1: Line, line2: Line) -> bool:
        """2直線が同一直線か判定します。"""
        return line1 == line2
