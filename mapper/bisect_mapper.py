import bisect


class bisectMapper:
    """bisectを個人的にわかりやすいようにしたかったやつ"""
    def __init__(self, A = [], sort=True) -> None:
        self.data = A
        if sort and len(A) > 0:
            self.data.sort()
        self.N = len(A)

    def set_data(self, A):
        """データをセットし直します"""
        self.data = A
        self.N = len(A)

    def data_leq(self, a):
        """
        a以下のデータの最大のインデックスを取得します．
        aがデータ内の最小値より小さければ-1を返却します．
        """
        tmp = bisect.bisect_right(self.data, a)
        if tmp == self.N:
            return self.N - 1
        return tmp if self.data[tmp] == a else tmp - 1

    def data_geq(self, a):
        """
        a以上のデータの最小のインデックスを取得します
        aがデータ内の最大値より大きければNを返却します．
        """
        tmp = bisect.bisect_left(self.data, a)
        if tmp == -1:
            return 0
        return bisect.bisect_left(self.data, a)

    def data_l(self, a):
        """
        a未満のデータの最大のインデックスを取得します．
        aがデータ内の最大値より大きければN，小さければ-1を返却します．
        """
        tmpl = self.data_leq(a)
        tmpr = self.data_geq(a)
        # 枠からはみ出た場合
        if tmpl == -1:
            return tmpl
        if tmpl == self.N:
            return self.N - 1
        # ちょうどのデータだった場合
        if self.data[tmpl] == a:
            return tmpr - 1
        return tmpl

    def data_g(self, a):
        """
        a超過のデータの最小のインデックスを取得します
        aがデータ内の最大値より大きければN，小さければ0を返却します．
        """
        tmpl = self.data_leq(a)
        tmpr = self.data_geq(a)
        # 枠からはみ出た場合
        if tmpr == self.N:
            return tmpr
        # ちょうどのデータだった場合
        if self.data[tmpr] == a:
            return tmpl + 1
        return tmpr

    def between_c_c(self, a, b):
        """a以上b以下のデータの個数を取得します"""
        # a以下となる最大のインデックス
        tmp = self.data_geq(a)
        # はみ出た結果の場合
        if tmp == -1:
            tmp = 0
        if tmp == self.N:
            tmp = self.N - 1
        if self.data[tmp] < a:
            tmp += 1
        tmpl = tmp
        # b以上となる最小のインデックス
        tmp = self.data_leq(b)
        if tmp == -1:
            tmp = 0
        if tmp == self.N:
            tmp = self.N - 1
        if self.data[tmp] > b:
            tmp -= 1
        tmpr = tmp
        return tmpr - tmpl + 1

    def between_c_o(self, a, b):
        """a以上b未満のデータの個数を取得します"""
        # a以下となる最大のインデックス
        tmp = self.data_geq(a)
        # はみ出た結果の場合
        if tmp == -1:
            tmp = 0
        if tmp == self.N:
            tmp = self.N - 1
        if self.data[tmp] < a:
            tmp += 1
        tmpl = tmp
        # b超過となる最小のインデックス
        tmp = self.data_l(b)
        if tmp == -1:
            tmp = 0
        if tmp == self.N:
            tmp = self.N - 1
        tmpr = tmp
        return tmpr - tmpl + 1

    def between_o_c(self, a, b):
        """a超過b以下のデータの個数を取得します"""
        # a超過となる最大のインデックス
        tmp = self.data_g(a)
        # はみ出た結果の場合
        if tmp == -1:
            tmp = 0
        if tmp == self.N:
            tmp = self.N - 1
        tmpl = tmp
        # b以上となる最小のインデックス
        tmp = self.data_geq(b)
        if tmp == -1:
            tmp = 0
        if tmp == self.N:
            tmp = self.N - 1
        if self.data[tmp] > b:
            tmp -= 1
        tmpr = tmp
        return tmpr - tmpl + 1

    def between_o_o(self, a, b):
        """a超過b未満のデータの個数を取得します"""
        # a以下となる最大のインデックス
        tmp = self.data_g(a)
        # はみ出た結果の場合
        if tmp == -1:
            tmp = 0
        if tmp == self.N:
            tmp = self.N - 1
        tmpl = tmp
        # b超過となる最小のインデックス
        tmp = self.data_l(b)
        if tmp == -1:
            tmp = 0
        if tmp == self.N:
            tmp = self.N - 1
        tmpr = tmp
        return tmpr - tmpl + 1


# # *** Example (ABC248 D) ***
N = int(input())
A = [int(l) for l in input().split()]
Q = int(input())
data = dict()
for idx in range(N):
    a = A[idx]
    tmp = data.get(a, [])
    tmp.append(idx)
    data[a] = tmp
bm = bisectMapper()
result = []
for q in range(Q):
    L, R, X = [int(l) for l in input().split()]
    L, R = L - 1, R - 1
    dat = data.get(X, [])
    if len(dat) == 0:
        result.append(0)
    else:
        bm.set_data(dat)
        res = bm.between_c_c(L, R)
        result.append(res)

for r in result:
    print(r)
