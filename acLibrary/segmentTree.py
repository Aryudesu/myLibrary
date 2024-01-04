# セグ木
class segtree:
    __n = 0
    __size = 0
    __log = 0
    __data = []
    __e = 1

    def __update(self, k):
        """データ更新"""
        self.__data[k] = self.__func(self.__data[2 * k], self.__data[2 * k + 1])

    def bit_ceil(self, n):
        """ビット上げ"""
        x = 1
        while x < n:
            x *= 2
        return x

    def countr_zero(self, n):
        """ビットの右側の0の個数を調べる"""
        if n == 0:
            return 0
        tmp = n
        res = 1
        while tmp != 0:
            tmp >>= 1
            res += 1
        return res

    def __init__(self, v, e, f) -> None:
        """コンストラクタ"""
        self.__e = e
        self.__func = f
        self.__n = len(v)
        self.__size = self.bit_ceil(self.__n)
        self.__log = self.countr_zero(self.__size)
        self.__data = [e] * (2 * self.__size)
        for i in range(self.__n):
            self.__data[self.__size + i] = v[i]
        for i in range(self.__size - 1, 0, -1):
            self.__update(i)

    def set(self, p, x):
        """データをセット"""
        assert 0 <= p and p < self.__n
        p += self.__size
        self.__data[p] = x
        for i in range(1, self.__log + 1):
            self.__update(p >> i)

    def get(self, p):
        """データ取得"""
        assert 0 <= p and p < self.__n
        return self.__data[p + self.__size]

    def prod(self, l, r):
        """相乗取得"""
        assert 0 <= l and l <= r and r <= self.__n
        sml = self.__e
        smr = self.__e
        l += self.__size
        r += self.__size
        while l < r:
            if l & 1:
                sml = self.__func(sml, self.__data[l])
                l += 1
            if r & 1:
                r -= 1
                smr = self.__func(self.__data[r], smr)
            l >>= 1
            r >>= 1
        return self.__func(sml, smr)

    def all_prod(self):
        """すべての相乗取得"""
        return self.__data[1]

    def max_right(self, l, f):
        """二分探索"""
        assert 0 <= l and l <= self.__n
        assert f(self.__e)
        if l == self.__n:
            return self.__n
        l += self.__size
        sm = self.__e
        while True:
            while l % 2 == 0:
                l >>= 1
            if not f(self.__func(sm, self.__data[l])):
                while l < self.__size:
                    l = 2 * l
                    if f(self.__func(sm, self.__data[l])):
                        sm = self.__func(sm, self.__data[l])
                        l += 1
                return l - self.__size
            sm = self.__func(sm, self.__data[l])
            l += 1
            if (l & -l) == l:
                break
        return self.__n

    def min_left(self, r, f):
        """二分探索"""
        assert 0 <= r and r <= self.__n
        assert f(self.__e)
        if r == 0:
            return 0
        r += self.__size
        sm = self.__e
        while True:
            r -= 1
            while r > 1 and (r % 2):
                r >>= 1
            if not f(self.__func(self.__data[r], sm)):
                while r < self.__size:
                    r = 2 * r + 1
                    if f(self.__func(self.__data[r], sm)):
                        sm = self.__func(self.__data[r], sm)
                        r -= 1
                return r + 1 - self.__size
            if (r & -r) == r:
                break
        return 0


target = 0

# 積の計算
def prod_func(x, y):
    return max([x, y])

# ソート用
def f_func(v):
    return v < target

N, Q = [int(l) for l in input().split()]
A = [int(l) for l in input().split()]
st = segtree(A, -1, prod_func)

result = []
for q in range(Q):
    T, X, Y = [int(l) for l in input().split()]
    if T == 1:
        st.set(X-1, Y)
    elif T == 2:
        result.append(st.prod(X-1, Y))
    elif T == 3:
        target = Y
        result.append(st.max_right(X-1, f_func) + 1)

for r in result:
    print(r)