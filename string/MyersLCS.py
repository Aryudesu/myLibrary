class MyersLCS:
    """
    Myers O(ND) LCS

    - LCS length
    - LCS restore
    - SES restore
    """

    def __init__(self, A, B):
        self.A = A
        self.B = B

        self.N = len(A)
        self.M = len(B)

        self.trace = []
        self.D = 0

        self._built = False

    def build(self):

        A = self.A
        B = self.B

        N = self.N
        M = self.M

        MAX = N + M
        OFFSET = MAX

        V = [0] * (2 * MAX + 1)

        trace = []

        for D in range(MAX + 1):

            trace.append(V[:])

            for k in range(-D, D + 1, 2):

                idx = k + OFFSET

                if k == -D:
                    x = V[idx + 1]

                elif k == D:
                    x = V[idx - 1] + 1

                elif V[idx - 1] < V[idx + 1]:
                    x = V[idx + 1]

                else:
                    x = V[idx - 1] + 1

                y = x - k

                while x < N and y < M and A[x] == B[y]:
                    x += 1
                    y += 1

                V[idx] = x

                if x >= N and y >= M:
                    self.trace = trace
                    self.D = D
                    self._built = True
                    return

    def _backtrack(self):
        if not self._built:
            self.build()

        A = self.A
        B = self.B

        x = self.N
        y = self.M

        MAX = self.N + self.M
        OFFSET = MAX
        result = []
        for D in range(self.D, 0, -1):
            V = self.trace[D]
            k = x - y
            idx = k + OFFSET
            if k == -D:
                prev_k = k + 1
            elif k == D:
                prev_k = k - 1
            elif V[idx - 1] < V[idx + 1]:
                prev_k = k + 1
            else:
                prev_k = k - 1
            prev_idx = prev_k + OFFSET

            prev_x = V[prev_idx]
            prev_y = prev_x - prev_k

            while x > prev_x and y > prev_y:
                result.append(("match", A[x - 1]))
                x -= 1
                y -= 1

            if x == prev_x:
                result.append(("insert", B[y - 1]))
                y -= 1
            else:
                result.append(("delete", A[x - 1]))
                x -= 1

        while x > 0 and y > 0:
            result.append(("match", A[x - 1]))
            x -= 1
            y -= 1
        result.reverse()
        return result

    def get_lcs(self):
        data = self._backtrack()
        lcs = [v for typ, v in data if typ == "match"]
        if isinstance(self.A, str):
            return "".join(lcs)
        return lcs

    def get_lcs_length(self):
        if not self._built:
            self.build()
        return (self.N + self.M - self.D) // 2

    def get_ses(self):
        return self._backtrack()
    

S = input()
T = input()
lcs = MyersLCS(S, T)
print(lcs.get_lcs())
