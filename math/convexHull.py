from typing import TypeAlias

Point: TypeAlias = tuple[int, int]


def cross(a: Point, b: Point, c: Point) -> int:
    """外積 (b-a) x (c-a)"""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def convexHull(points: list[Point], includeCollinear: bool = False) -> list[Point]:
    """
    凸包を反時計回りで返す。
    include_collinear=False: 辺上の点を除く
    include_collinear=True : 辺上の点も含める
    """
    points = sorted(set(points))
    n = len(points)

    if n <= 1:
        return points

    def shouldPop(a: Point, b: Point, c: Point) -> bool:
        cr = cross(a, b, c)
        if includeCollinear:
            return cr < 0
        else:
            return cr <= 0

    lower = []
    for p in points:
        while len(lower) >= 2 and shouldPop(lower[-2], lower[-1], p):
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and shouldPop(upper[-2], upper[-1], p):
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]


def polygonArea2(poly: list[Point]) -> int:
    """多角形の面積の2倍を返す。頂点は時計回り/反時計回りどちらでもOK。"""
    n = len(poly)
    area2 = 0

    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        area2 += x1 * y2 - y1 * x2

    return abs(area2)

# === AWC0103 E
N = int(input())
XY = []
for n in range(N):
    x, y = map(int, input().split())
    XY.append((x, y))

print(polygonArea2(convexHull(XY)))
