from math import gcd


class LineIdentifier:
    """2点を結ぶ直線 ax + by + c = 0 の(a,b,c)を返却する．"""

    @staticmethod
    def from_points(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1
        a = dy
        b = -dx
        c = dx * y1 - dy * x1
        g = gcd(gcd(abs(a), abs(b)), abs(c))
        a //= g
        b //= g
        c //= g
        if a < 0 or (a == 0 and b < 0):
            a *= -1
            b *= -1
            c *= -1
        return (a, b, c)
