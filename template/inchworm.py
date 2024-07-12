class inchworm:
    """尺取法のテンプレート"""

    def __init__(self, d = []) -> None:
        self.N = len(d)
        self.data = d
        self.orig_init()

    def set_data(self, d):
        self.N = len(d)
        self.data = d
        self.orig_init()

    def orig_init(self):
        """適宜必要なものがあれば設定"""
        # TODO
        self.num_set = set()
        self.num_count = dict()
        self.sum_data = 0
        self.result = 0

    def is_ok(self, r, x):
        """
        右側更新時に条件を満たしているかの判定を行います
        ===
        @param r 右側インデックス
        @param x クエリ内容
        """
        # TODO
        dat = self.data[r]
        if not dat in self.num_set:
            return len(self.num_set) + 1 <= x
        return len(self.num_set) <= x

    def update_r(self, r):
        """
        右側更新時の挙動を設定します
        """
        # TODO
        tmp = self.data[r]
        self.num_count[tmp] = self.num_count.get(tmp, 0) + 1
        self.num_set.add(tmp)

    def update_l(self, l):
        """
        左側更新時の挙動を設定します
        """
        # TODO
        tmp = self.data[l]
        self.num_count[tmp] = self.num_count.get(tmp, 0) - 1
        if self.num_count[tmp] <= 0:
            self.num_set.discard(tmp)

    def update_result(self, width):
        """
        区間の広さを引数とし結果データの更新を行います
        """
        # TODO
        self.result = max([self.result, width])

    def calc(self, query):
        """尺取法を行います"""
        x = query
        r = 0
        for l in range(self.N):
            # [l r)の区間について
            while r < self.N and self.is_ok(r, x):
                self.update_r(r)
                r += 1
            self.update_result(r - l)
            if l == r:
                r += 1
            else:
                self.update_l(l)
        return self.result


N, K = [int(l) for l in input().split()]
A = [int(l) for l in input().split()]
iw = inchworm(A)
print(iw.calc(K))
