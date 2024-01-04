class internalBit:
    def bit_ceil(self, n):
        x = 1
        while x < n:
            x *= 2
        return x

    def countr_zero(self, n):
        if n == 0:
            return 0
        tmp = n
        res = 1
        while tmp != 0:
            tmp >>= 1
            res += 1
        return res

    def countr_zero_constexpr(n):
        x = 0
        while not n & (1 << x): x += 1
        return x
