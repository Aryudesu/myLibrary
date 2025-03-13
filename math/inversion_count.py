class BIT:
    def __init__(self, n):
        """要素数nで初期化する"""
        self.n = n
        self.tree = [0] * (n + 1)

    def add(self, idx, val):
        """idxにvalを加算する"""
        while idx <= self.n:
            self.tree[idx] += val
            idx += idx & -idx

    def sum(self, idx):
        """idxまでの累積わを求める"""
        res = 0
        while idx > 0:
            res += self.tree[idx]
            idx -= idx & -idx
        return res

    def range_sum(self, left, right):
        """区間[left, right]の和を求める"""
        return self.sum(right) - self.sum(left - 1)


def inversion_count(arr):
    """
    転倒数を計算する
    """
    sorted_arr = sorted(set(arr))
    compress = {val: i + 1 for i, val in enumerate(sorted_arr)}
    bit = BIT(len(sorted_arr))
    inv_count = 0
    for i in reversed(range(len(arr))):
        inv_count += bit.sum(compress[arr[i]] - 1)
        bit.add(compress[arr[i]], 1)

    return inv_count
