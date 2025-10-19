class Partition:
    def __init__(self, num = 4*(10**4), mod:int = 0):
        """numまでの分割数をmodで割ったあまり（0の場合は剰余を考慮しない）で計算します"""
        self.num = num
        self.mod = mod
        self.penta = self._calcPentagon(num)
        self.data = [1]
        for i in range(1, num + 1):
            self.data.append(self._partition(i, self.data))
    
    def _calcPentagon(self, num: int) -> list:
        """五角数と符号の事前計算を行います"""
        result = []
        for i in range(1, num + 1):
            g1, g2 = i * (3 * i - 1) // 2, i * (3 * i + 1) // 2
            if g1 > num and g2 > num:
                break
            sign = 1 if i % 2 else -1
            if g1 <= num:
                result.append((g1, sign))
            if g2 <= num:
                result.append((g2, sign))
        result.sort()
        return result

    def _partition(self, num: int, mem: list)-> int:
        """DPによる分割数計算"""
        result = 0
        for g, sgn in self.penta:
            if num < g:
                break
            result += sgn * mem[num - g]
            if self.mod > 0:
                result %= self.mod
        return result

    def getPartition(self, num: int) -> int:
        """numに対しての分割数を取得します"""
        assert self.num >= num
        return self.data[num]

    def getPartitionList(self) -> list:
        """分割数をリストで返却します"""
        return self.data

# === sample
pt = Partition(4*(10**4), 998244353)
Q = int(input())
for q in range(Q):
    print(pt.getPartition(int(input())))
