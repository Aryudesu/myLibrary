from fractions import Fraction
from math import gcd, hypot

Point = tuple[int, int]
Line = tuple[int, int, int]
Segment = tuple[Point, Point]

class LineUtil:
    @staticmethod
    def normalize(a: int, b: int, c: int) -> Line:
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
    def from_points(p: Point, q: Point) -> Line:
        if p == q:
            raise ValueError("異なる2点を指定してください")

        x1, y1 = p
        x2, y2 = q

        return LineUtil.normalize(
            y2 - y1,
            x1 - x2,
            x2 * y1 - x1 * y2,
        )

    @staticmethod
    def perpendicular_bisector(p: Point, q: Point) -> Line:
        if p == q:
            raise ValueError("異なる2点を指定してください")

        x1, y1 = p
        x2, y2 = q

        return LineUtil.normalize(
            2 * (x1 - x2),
            2 * (y1 - y2),
            x2 * x2 + y2 * y2 - x1 * x1 - y1 * y1,
        )

    @staticmethod
    def evaluate(line: Line, p: Point) -> int:
        a, b, c = line
        x, y = p
        return a * x + b * y + c

    @staticmethod
    def contains(line: Line, p: Point) -> bool:
        return LineUtil.evaluate(line, p) == 0

    @staticmethod
    def is_parallel(line1: Line, line2: Line) -> bool:
        a1, b1, _ = line1
        a2, b2, _ = line2
        return a1 * b2 == a2 * b1

    @staticmethod
    def is_same(line1: Line, line2: Line) -> bool:
        """
        正規化済みの直線同士を比較する。
        """
        return line1 == line2

    @staticmethod
    def distance_to_point(line: Line, p: Point) -> float:
        a, b, _ = line
        return abs(LineUtil.evaluate(line, p)) / hypot(a, b)

    @staticmethod
    def intersection(
        line1: Line,
        line2: Line,
    ) -> tuple[Fraction, Fraction] | None:
        a1, b1, c1 = line1
        a2, b2, c2 = line2

        det = a1 * b2 - a2 * b1
        if det == 0:
            return None

        x = Fraction(b1 * c2 - b2 * c1, det)
        y = Fraction(c1 * a2 - c2 * a1, det)

        return x, y
