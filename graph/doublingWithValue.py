class DoublingWithValue:
    def __init__(self, nxt, val, op, e, max_pow=60):
        """
        nxt[v] : 次の遷移先
        val[v] : 1回遷移で得られる値
        op(a, b, k) : 値の合成関数
            a: 前半
            b: 後半
            k: 後半ブロックの指数（長さ = 2^k）
        e : 単位元
        """
        self.N = len(nxt)
        self.M = max_pow
        self.op = op
        self.e = e

        self.nxt = [nxt[:]]
        self.val = [val[:]]

        for k in range(1, self.M):
            prev_nxt = self.nxt[-1]
            prev_val = self.val[-1]

            next_nxt = [0] * self.N
            next_val = [0] * self.N

            for v in range(self.N):
                mid = prev_nxt[v]
                next_nxt[v] = prev_nxt[mid]
                next_val[v] = op(prev_val[v], prev_val[mid], k - 1)

            self.nxt.append(next_nxt)
            self.val.append(next_val)

    def jump(self, v, t):
        res = self.e
        pos = v
        for k in range(t.bit_length()):
            if t >> k & 1:
                res = self.op(res, self.val[k][pos], k)
                pos = self.nxt[k][pos]
        return res, pos
    

N, Q, M = map(int, input().split())

digit = []
to = []

for _ in range(N):
    d, p = map(int, input().split())
    digit.append(d)
    to.append(p - 1)

pow10 = [10 % M]
for _ in range(60):
    pow10.append(pow10[-1] * pow10[-1] % M)

def op(a, b, k):
    return (a * pow10[k] + b) % M

db = DoublingWithValue(to, digit, op, 0, 61)

for _ in range(Q):
    s, K = map(int, input().split())
    ans, _ = db.jump(s - 1, K)
    print(ans)
