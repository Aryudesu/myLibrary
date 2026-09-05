from .pointUtil import Point, PointUtil


class PolygonUtil:
    """
    多角形に関する幾何ユーティリティ。

    頂点は周上の順番（時計回り / 反時計回りのどちらでも可）で与える。
    自己交差しない単純多角形を想定する。
    """

    @staticmethod
    def edge_moment(p: Point, q: Point) -> tuple[int, int, int]:
        """
        有向辺 p -> q の面積・一次モーメントへの寄与を返す。

        戻り値:
            (area2, centroid_x_numerator, centroid_y_numerator)

        area2:
            符号付き面積の2倍への寄与 cross(p, q)

        centroid_x_numerator / centroid_y_numerator:
            多角形の重心を
                Gx = sx / (3 * area2)
                Gy = sy / (3 * area2)
            と表したときの sx, sy への寄与。

        すべて整数演算で計算できる。
        """
        c = PointUtil.cross(p, q)
        return (
            c,
            (p[0] + q[0]) * c,
            (p[1] + q[1]) * c,
        )

    @staticmethod
    def signed_area2(poly: list[Point]) -> int:
        """
        多角形の符号付き面積の2倍を返す。

        反時計回りなら正、時計回りなら負。
        頂点数が3未満の場合は0を返す。
        """
        n = len(poly)
        if n < 3:
            return 0

        area2 = 0
        for i in range(n):
            area2 += PointUtil.cross(poly[i], poly[(i + 1) % n])
        return area2

    @staticmethod
    def area2(poly: list[Point]) -> int:
        """多角形の面積の2倍（非負整数）を返す。"""
        return abs(PolygonUtil.signed_area2(poly))

    @staticmethod
    def area(poly: list[Point]) -> float:
        """多角形の面積を返す。"""
        return PolygonUtil.area2(poly) / 2

    @staticmethod
    def centroid(poly: list[Point]) -> tuple[float, float]:
        """
        一様密度の単純多角形の重心を返す。

        時計回り・反時計回りのどちらでも同じ重心を返す。
        面積0の退化多角形では ValueError を送出する。
        """
        n = len(poly)
        if n < 3:
            raise ValueError("重心の計算には3頂点以上が必要です")

        area2 = 0
        sx = 0
        sy = 0

        for i in range(n):
            da, dx, dy = PolygonUtil.edge_moment(
                poly[i], poly[(i + 1) % n]
            )
            area2 += da
            sx += dx
            sy += dy

        if area2 == 0:
            raise ValueError("面積0の多角形の重心は計算できません")

        denominator = 3 * area2
        return sx / denominator, sy / denominator

    @staticmethod
    def moment(poly: list[Point]) -> tuple[int, int, int]:
        """
        多角形全体の (area2, sx, sy) を整数で返す。

        centroid() と同じ定義で、
            Gx = sx / (3 * area2)
            Gy = sy / (3 * area2)
        となる。

        区間累積和などで辺寄与を扱いたい場合に利用できる。
        """
        n = len(poly)
        if n == 0:
            return 0, 0, 0

        area2 = 0
        sx = 0
        sy = 0

        for i in range(n):
            da, dx, dy = PolygonUtil.edge_moment(
                poly[i], poly[(i + 1) % n]
            )
            area2 += da
            sx += dx
            sy += dy

        return area2, sx, sy
