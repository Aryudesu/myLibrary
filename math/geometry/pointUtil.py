Point = tuple[int, int]

class PointUtil:
    @staticmethod
    def add(p: Point, q: Point) -> Point:
        return p[0] + q[0], p[1] + q[1]

    @staticmethod
    def sub(p: Point, q: Point) -> Point:
        return p[0] - q[0], p[1] - q[1]

    @staticmethod
    def dot(p: Point, q: Point) -> int:
        return p[0] * q[0] + p[1] * q[1]

    @staticmethod
    def cross(p: Point, q: Point) -> int:
        return p[0] * q[1] - p[1] * q[0]

    @staticmethod
    def orient(a: Point, b: Point, c: Point) -> int:
        """
        正: 反時計回り
        負: 時計回り
        0: 一直線上
        """
        return PointUtil.cross(
            PointUtil.sub(b, a),
            PointUtil.sub(c, a),
        )

    @staticmethod
    def norm2(p: Point) -> int:
        return PointUtil.dot(p, p)

    @staticmethod
    def distance2(p: Point, q: Point) -> int:
        return PointUtil.norm2(PointUtil.sub(p, q))
