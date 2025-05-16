from atcoder.lazysegtree import LazySegTree


class LazySegBase:
    def __init__(self, lst):
        self.lst = LazySegTree(
            self.op, self.e(), self.mapping, self.composition, self.id(), lst
        )

    def set(self, p, x):
        self.lst.set(p, x)

    def get(self, p):
        return self.lst.get(p)

    def prod(self, l, r):
        return self.lst.prod(l, r)

    def all_prod(self):
        return self.lst.all_prod()

    def apply(self, l, r, f):
        self.lst.apply(l, r, f)


class LazySegChmax(LazySegBase):
    """
    ACL LazySegTree 用設定:

    * op(a, b): セグメント木に乗る要素の二項演算
        例：min(a, b), max(a, b), a + b など
    * mapping(f, x): 遅延評価値 f を値 x に適用
        ex: "加算": f + x, "chmax": max(f, x), "代入": f
    * composition(f, g): 遅延値同士の合成（f を先に適用）
        ex: "加算": f + g, "代入": f（g を無視）
    * e(): 本体データの単位元
    * id(): 遅延データの単位元（影響を与えない値）
    """

    def op(self, a, b):
        return max(a, b)

    def mapping(self, f, x):
        return max(f, x)

    def composition(self, f, g):
        return max(f, g)

    def e(self):
        return -(10**10)

    def id(self):
        return -(10**10)


# === ABC382F

H, W, N = [int(l) for l in input().split()]
ls = [0] * W
lst = LazySegChmax(ls)
data = []
for n in range(N):
    tmp = [int(l) for l in input().split()]
    tmp[1] -= 1
    tmp.append(n)
    data.append(tmp)
data.sort(reverse=True)
result = []
for dat in data:
    y, x, l, num = dat
    h = lst.prod(x, x + l)
    lst.apply(x, x + l, h + 1)
    result.append([num, H - h])
result.sort()
for r in result:
    print(r[1])
