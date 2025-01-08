class SparseTable:
    def __init__(self, array):
        self.n = len(array)
        self.k = (self.n - 1).bit_length()
        self.table = [[0] * self.n for _ in range(self.k)]
        self.log = [0] * (self.n + 1)

        for i in range(self.n):
            self.table[0][i] = array[i]

        for i in range(2, self.n + 1):
            self.log[i] = self.log[i // 2] + 1

        for j in range(1, self.k):
            for i in range(self.n - (1 << j) + 1):
                self.table[j][i] = min(self.table[j - 1][i], self.table[j - 1][i + (1 << (j - 1))])

    def query(self, left, right):
        j = self.log[right - left]
        return min(self.table[j][left], self.table[j][right - (1 << j)])

arr = [1, 3, 2, 7, 9, 11, 3, 5]
st = SparseTable(arr)

print(st.query(2, 7))
