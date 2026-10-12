"""ACL LazySegTree の設定を再利用するためのテンプレート。"""

from atcoder.lazysegtree import LazySegTree


class LazySegMapper:
    """遅延セグ木の演算を派生クラスで設定するためのラッパー。

    派生クラスでは以下の5つのメソッドを定義する。

    - op(a, b): 区間情報を左 a、右 b の順序で結合
    - e(): 区間情報の単位元
    - mapping(f, x): 遅延操作 f を区間情報 x に適用
    - composition(f, g): g を適用した後に f を適用する操作（f ∘ g）
    - id(): 遅延操作の単位元

    インデックスは 0-indexed、区間は半開区間 [l, r)。
    max_right / min_left の述語は単位元 e() に対して True を返す必要がある。
    """

    def __init__(self, data):
        self.lst = LazySegTree(
            self.op, self.e(), self.mapping, self.composition, self.id(), data
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
        """半開区間 [l, r) に遅延操作 f を適用する。"""
        self.lst.apply(l, r, f)

    def max_right(self, l, predicate):
        return self.lst.max_right(l, predicate)

    def min_left(self, r, predicate):
        return self.lst.min_left(r, predicate)


# 旧名称を使ったコードとの互換性のために残す。
LazySegBase = LazySegMapper


class LazySegChmax(LazySegMapper):
    """区間 chmax（各要素を max(元の値, f) に変更）・区間最大値。"""

    def op(self, a, b):
        return max(a, b)

    def mapping(self, f, x):
        return max(f, x)

    def composition(self, f, g):
        return max(f, g)

    def e(self):
        return float("-inf")

    def id(self):
        return float("-inf")


class LazySegRangeAddMin(LazySegMapper):
    """区間加算・区間最小値取得。"""

    def op(self, a, b):
        return min(a, b)

    def mapping(self, f, x):
        return f + x

    def composition(self, f, g):
        return f + g

    def e(self):
        return float("inf")

    def id(self):
        return 0


def _example_main():
    """元のテンプレートに含まれていた利用例（直接実行したときだけ動作）。"""
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


if __name__ == "__main__":
    _example_main()
