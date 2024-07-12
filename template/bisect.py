class bisect_search:
    def __init__(self, is_ok, data = [], sort = True) -> None:
        if sort:
            data.sort()
        self.data = data
        self.is_ok = is_ok

    def search_left(self):
        """
        左側に対しての判定で二分探索実行
        ===
        return (条件を満たす中で最大, 条件を満たさない中で最小)
        """
        l = -1
        r = len(self.data)
        while r - l > 1:
            mid = (l + r) // 2
            if self.is_ok(mid):
                l = mid
            else:
                r = mid
        return l, r

    def search_right(self):
        """
        右側に対しての判定で二分探索実行
        ===
        return (条件を満たさない中で最大, 条件を満たす中で最小)
        """
        l = -1
        r = len(self.data)
        while r - l > 1:
            mid = (l + r) // 2
            if self.is_ok(mid):
                r = mid
            else:
                l = mid
        return l, r


