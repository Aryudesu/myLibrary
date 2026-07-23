from enum import IntEnum

Point = tuple[int, int]
Line = tuple[int, int, int]
Segment = tuple[Point, Point]

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


class SegmentIntersection(IntEnum):
    NONE = 0
    TOUCH = 1
    CROSS = 2
    OVERLAP = 3


class SegmentUtil:
    @staticmethod
    def contains(segment: Segment, p: Point) -> bool:
        a, b = segment

        if PointUtil.orient(a, b, p) != 0:
            return False

        return (
            min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])
        )

    @staticmethod
    def intersection_type(
        segment1: Segment,
        segment2: Segment,
    ) -> SegmentIntersection:
        a, b = segment1
        c, d = segment2

        o1 = PointUtil.orient(a, b, c)
        o2 = PointUtil.orient(a, b, d)
        o3 = PointUtil.orient(c, d, a)
        o4 = PointUtil.orient(c, d, b)

        if o1 == o2 == o3 == o4 == 0:
            return SegmentUtil._collinear_intersection_type(
                segment1,
                segment2,
            )

        if o1 * o2 < 0 and o3 * o4 < 0:
            return SegmentIntersection.CROSS

        if (
            (o1 == 0 and SegmentUtil.contains(segment1, c))
            or (o2 == 0 and SegmentUtil.contains(segment1, d))
            or (o3 == 0 and SegmentUtil.contains(segment2, a))
            or (o4 == 0 and SegmentUtil.contains(segment2, b))
        ):
            return SegmentIntersection.TOUCH

        return SegmentIntersection.NONE

    @staticmethod
    def _collinear_intersection_type(
        segment1: Segment,
        segment2: Segment,
    ) -> SegmentIntersection:
        a, b = segment1
        c, d = segment2

        # x方向に長さがあればx座標、それ以外はy座標で比較
        if a[0] != b[0] or c[0] != d[0]:
            left = max(min(a[0], b[0]), min(c[0], d[0]))
            right = min(max(a[0], b[0]), max(c[0], d[0]))
        else:
            left = max(min(a[1], b[1]), min(c[1], d[1]))
            right = min(max(a[1], b[1]), max(c[1], d[1]))

        if left > right:
            return SegmentIntersection.NONE
        if left == right:
            return SegmentIntersection.TOUCH
        return SegmentIntersection.OVERLAP

    @staticmethod
    def intersects(
        segment1: Segment,
        segment2: Segment,
    ) -> bool:
        return (
            SegmentUtil.intersection_type(segment1, segment2)
            != SegmentIntersection.NONE
        )

    @staticmethod
    def properly_intersects(
        segment1: Segment,
        segment2: Segment,
    ) -> bool:
        return (
            SegmentUtil.intersection_type(segment1, segment2)
            == SegmentIntersection.CROSS
        )

    @staticmethod
    def distance_to_point(
        segment: Segment,
        p: Point,
    ) -> float:
        a, b = segment

        ab = PointUtil.sub(b, a)
        ap = PointUtil.sub(p, a)

        length2 = PointUtil.norm2(ab)

        if length2 == 0:
            return PointUtil.distance2(a, p) ** 0.5

        projection = PointUtil.dot(ap, ab)

        if projection <= 0:
            return PointUtil.distance2(a, p) ** 0.5

        if projection >= length2:
            return PointUtil.distance2(b, p) ** 0.5

        return abs(PointUtil.cross(ab, ap)) / length2 ** 0.5

    @staticmethod
    def distance(
        segment1: Segment,
        segment2: Segment,
    ) -> float:
        if SegmentUtil.intersects(segment1, segment2):
            return 0.0

        a, b = segment1
        c, d = segment2

        return min(
            SegmentUtil.distance_to_point(segment1, c),
            SegmentUtil.distance_to_point(segment1, d),
            SegmentUtil.distance_to_point(segment2, a),
            SegmentUtil.distance_to_point(segment2, b),
        )
