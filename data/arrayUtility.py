import math

class arrayUtility:
    """配列で便利な機能等まとめたい"""
    def __init__(self, a: list = []):
        self.data = a

    def append(self, d):
        self.data.append(d)

    def inversion(self):
        """転倒数の計算"""
        if not self.data:
            return 0
        tmp = sorted(self.data)
        num = {tmp[i]: i + 1 for i in range(len(tmp))}
        compressed = [num[val] for val in self.data]
        n = len(compressed)
        bit = [0] * (n + 1)
        inv_count = 0
        def add(index, value):
            while index <= n:
                bit[index] += value
                index += index & -index
        def sum(index):
            s = 0
            while index > 0:
                s += bit[index]
                index -= index & -index
            return s
        for i in range(n - 1, -1, -1):
            inv_count += sum(compressed[i] - 1)
            add(compressed[i], 1)
        return inv_count

    def prefix_sum(self):
        """累積和"""
        result = [0]
        for i in range(len(self.data)):
            result.append(result[i] + self.data[i])
        return result

data = arrayUtility([3, 1, 2, 5, 4])
print(data.prefix_sum())
