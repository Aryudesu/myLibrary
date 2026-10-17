"""ACL LazySegTree に渡す5つの演算を差し替えて使うテンプレート。"""

from atcoder.lazysegtree import LazySegTree


_UNSET = object()


class LazySegMapper:
    """ACL LazySegTree の薄いラッパー。

    op / e / mapping / composition / id_ をコンストラクタで指定するだけで
    区間情報や遅延操作を変更できる。別の派生クラスを作る必要はない。

    - op(a, b): 左区間 a と右区間 b の情報を結合
    - e: 区間情報の単位元（値）
    - mapping(f, x): 遅延操作 f を区間情報 x に作用させる
    - composition(f, g): g の後に f を作用させる合成 f ∘ g
    - id_: 遅延操作の単位元（値）

    op などを省略した場合は同名のインスタンスメソッドを使うため、
    旧来の LazySegBase を継承して5関数を定義する使い方にも対応する。

    例（区間加算・区間最小値）::

        st = LazySegMapper(
            A,
            op=min,
            e=float('inf'),
            mapping=lambda f, x: f + x,
            composition=lambda f, g: f + g,
            id_=0,
        )
        st.apply(0, 3, 5)  # [0, 3) に +5
        answer = st.prod(0, 3)

    インデックスは 0-indexed、区間は半開区間 [l, r)。
    max_right / min_left の述語は、単位元 e に対して True が必要。
    """

    def __init__(self, data, *, op=None, e=_UNSET, mapping=None,
                 composition=None, id_=_UNSET):
        self.lst = LazySegTree(
            self.op if op is None else op,
            self.e() if e is _UNSET else e,
            self.mapping if mapping is None else mapping,
            self.composition if composition is None else composition,
            self.id() if id_ is _UNSET else id_,
            data,
        )

    # 継承方式を使う場合に、派生クラスで次の5メソッドを定義する。
    def op(self, a, b):
        raise NotImplementedError("op を指定してください")

    def e(self):
        raise NotImplementedError("e を指定してください")

    def mapping(self, f, x):
        raise NotImplementedError("mapping を指定してください")

    def composition(self, f, g):
        raise NotImplementedError("composition を指定してください")

    def id(self):
        raise NotImplementedError("id_ を指定してください")

    def set(self, p, x):
        self.lst.set(p, x)

    def get(self, p):
        return self.lst.get(p)

    def prod(self, l, r):
        return self.lst.prod(l, r)

    def all_prod(self):
        return self.lst.all_prod()

    def apply(self, *args):
        """一点作用 apply(p, f) または区間作用 apply(l, r, f)。"""
        self.lst.apply(*args)

    def max_right(self, l, predicate):
        return self.lst.max_right(l, predicate)

    def min_left(self, r, predicate):
        return self.lst.min_left(r, predicate)


# 旧名称で継承していたコードとの互換性を維持する。
LazySegBase = LazySegMapper


class LazySegChmax(LazySegMapper):
    """旧テンプレートとの互換用：区間 chmax・区間最大値。"""

    def op(self, a, b):
        return max(a, b)

    def e(self):
        return float("-inf")

    def mapping(self, f, x):
        return max(f, x)

    def composition(self, f, g):
        return max(f, g)

    def id(self):
        return float("-inf")


def _example_main():
    """旧ファイルに含まれていた利用例。直接実行した場合にのみ動作する。"""
    H, W, N = map(int, input().split())
    ls = [0] * W
    lst = LazySegMapper(
        ls,
        op=max,
        e=float("-inf"),
        mapping=max,
        composition=max,
        id_=float("-inf"),
    )
    data = []
    for n in range(N):
        y, x, l = map(int, input().split())
        data.append((y, x - 1, l, n))
    data.sort(reverse=True)
    result = []
    for y, x, l, num in data:
        h = lst.prod(x, x + l)
        lst.apply(x, x + l, h + 1)
        result.append((num, H - h))
    result.sort()
    for _, answer in result:
        print(answer)


if __name__ == "__main__":
    _example_main()
