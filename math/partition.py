class Partition:
    def __init__(self, num = 4*(10**4), mod:int = 0):
        """numまでの分割数をmodで割ったあまり（0の場合は剰余を考慮しない）で計算します"""
        self.num = num
        self.mod = mod
        self.data = [1]
        for i in range(1, num + 1):
            self.data.append(self._partition(i, self.data))

    def _partition(self, num: int, mem: list)-> int:
        """DPによる分割数計算"""
        result = 0
        for i in range(1, num + 1):
            g1, g2 = [i * (3 * i - 1) // 2, i * (3 * i + 1) // 2]
            if num < g1 and num < g2:
                break
            if num >= g1:
                result += mem[num - g1] if i % 2 else -mem[num - g1]
                if self.mod > 0:
                    result %= self.mod
            if num >= g2:
                result += mem[num - g2] if i % 2 else -mem[num - g2]
                if self.mod > 0:
                    result %= self.mod
        return result

    def getPartition(self, num: int) -> int:
        """numに対しての分割数を取得します"""
        assert self.num > num
        return self.data[num]

    def getPartitionList(self) -> list:
        """分割数をリストで返却します"""
        return self.data

pt = Partition(4*(10**4), 998244353)
Q = int(input())
for q in range(Q):
    print(pt.getParition(int(input())))

