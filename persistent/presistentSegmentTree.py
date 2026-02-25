class PresistentSegTree:
    def __init__(self, n: int, initArray: list[int]|None=None):
        self.nodes: list[list[int]] = []
        self.n = n
        if initArray is None:
            initArray = [0] * self.n
        assert len(initArray) == self.n
        self.root = self._build(0, n, initArray)

    def newNode(self, left: int, right: int, value: int)->int:
        self.nodes.append([left, right, value])
        return len(self.nodes) - 1

    def _build(self, l: int, r: int, arr: list[int])-> int:
        if r - l == 1:
            return self.newNode(-1, -1, arr[l])
        m = (l + r) // 2
        left= self._build(l, m, arr)
        right = self._build(m, r, arr)
        val = self.nodes[left][2] + self.nodes[right][2]
        return self.newNode(left, right, val)

    def update(self, prev: int, pos: int, newVal: int)-> int:
        return self._update(prev, 0, self.n, pos, newVal)

    def _update(self, node: int, l: int, r: int, pos: int, newVal: int) -> int:
        if r - l == 1:
            return self.newNode(-1, -1, newVal)
        m = (l + r) // 2
        left, right, _ = self.nodes[node]
        if pos < m:
            new_left = self._update(left, l, m, pos, newVal)
            new_right = right
        else:
            new_left = left
            new_right = self._update(right, m, r, pos, newVal)
        val = self.nodes[new_left][2] + self.nodes[new_right][2]
        return self.newNode(new_left, new_right, val)

    def query(self, root: int, ql: int, qr: int) -> int:
        return self._query(root, 0, self.n, ql, qr)

    def _query(self, node: int, l: int, r: int, ql: int, qr: int)-> int:
        if node == -1 or qr <= l or r <= ql:
            return 0
        if ql <= l and r <= qr:
            return self.nodes[node][2]
        m = (l + r) // 2
        left, right, _ = self.nodes[node]
        vl = self._query(left, l, m, ql, qr)
        vr = self._query(right, m, r, ql, qr)
        return vl + vr


# 初期配列
A = [1, 2, 3, 4, 5]
n = len(A)

seg = PresistentSegTree(n, A)

# ver0 の root
root0 = seg.root

# ver1: pos=2 を 10 に変更 (A[2] = 10)
root1 = seg.update(root0, 2, 10)

# ver2: ver1 から pos=4 を 100 に変更
root2 = seg.update(root1, 4, 100)

# それぞれ別バージョンでクエリ可能
print(seg.query(root0, 0, 5))  # 1+2+3+4+5 = 15
print(seg.query(root1, 0, 5))  # 1+2+10+4+5 = 22
print(seg.query(root2, 0, 5))  # 1+2+10+4+100 = 117

# 過去バージョンでの区間和
print(seg.query(root0, 1, 4))  # ver0 の [1,4) = 2+3+4 = 9
print(seg.query(root1, 1, 4))  # ver1 の [1,4) = 2+10+4 = 16
