import sys

input = sys.stdin.buffer.readline
sys.setrecursionlimit(1 << 25)


class InsertableList:
    """
    配列ベースのImplicit Treap。

    append            期待 O(log N)
    insert            期待 O(log N)
    popleft           期待 O(log N)
    pop               期待 O(log N)
    添字アクセス      期待 O(log N)
    """

    __slots__ = (
        "root",
        "value",
        "priority",
        "left",
        "right",
        "size",
        "rand_state",
    )

    def __init__(self):
        # 0番ノードをnullとして利用
        self.root = 0
        self.value = [0]
        self.priority = [0]
        self.left = [0]
        self.right = [0]
        self.size = [0]

        self.rand_state = 2463534242

    def __len__(self):
        return self.size[self.root]

    def _rand(self):
        """xorshift32"""
        x = self.rand_state
        x ^= x << 13
        x ^= x >> 17
        x ^= x << 5
        x &= 0xFFFFFFFF
        self.rand_state = x
        return x

    def _new_node(self, x):
        node = len(self.value)

        self.value.append(x)
        self.priority.append(self._rand())
        self.left.append(0)
        self.right.append(0)
        self.size.append(1)

        return node

    def _update(self, node):
        self.size[node] = (
            self.size[self.left[node]]
            + 1
            + self.size[self.right[node]]
        )

    def _merge(self, a, b):
        if a == 0:
            return b
        if b == 0:
            return a

        if self.priority[a] > self.priority[b]:
            self.right[a] = self._merge(self.right[a], b)
            self._update(a)
            return a

        self.left[b] = self._merge(a, self.left[b])
        self._update(b)
        return b

    def _split(self, root, k):
        """
        先頭k個と、それ以降に分割する。
        """
        if root == 0:
            return 0, 0

        left_size = self.size[self.left[root]]

        if k <= left_size:
            a, self.left[root] = self._split(self.left[root], k)
            self._update(root)
            return a, root

        self.right[root], b = self._split(
            self.right[root],
            k - left_size - 1,
        )
        self._update(root)
        return root, b

    def append(self, x):
        self.root = self._merge(
            self.root,
            self._new_node(x),
        )

    def appendleft(self, x):
        self.root = self._merge(
            self._new_node(x),
            self.root,
        )

    def insert(self, index, x):
        n = len(self)

        # list.insert準拠
        if index < 0:
            index = max(0, index + n)
        elif index > n:
            index = n

        a, b = self._split(self.root, index)
        node = self._new_node(x)

        self.root = self._merge(
            self._merge(a, node),
            b,
        )

    def popleft(self):
        if self.root == 0:
            raise IndexError("popleft from empty InsertableList")

        self.root, result = self._pop_leftmost(self.root)
        return result

    def _pop_leftmost(self, node):
        left = self.left[node]

        if left == 0:
            return self.right[node], self.value[node]

        self.left[node], result = self._pop_leftmost(left)
        self._update(node)
        return node, result

    def pop(self, index=-1):
        n = len(self)

        if n == 0:
            raise IndexError("pop from empty InsertableList")

        if index < 0:
            index += n

        if not 0 <= index < n:
            raise IndexError("InsertableList index out of range")

        a, b = self._split(self.root, index)
        target, c = self._split(b, 1)

        self.root = self._merge(a, c)
        return self.value[target]

    def __getitem__(self, index):
        n = len(self)

        if index < 0:
            index += n

        if not 0 <= index < n:
            raise IndexError("InsertableList index out of range")

        node = self.root

        while node:
            left_size = self.size[self.left[node]]

            if index < left_size:
                node = self.left[node]
            elif index == left_size:
                return self.value[node]
            else:
                index -= left_size + 1
                node = self.right[node]

        raise IndexError("InsertableList index out of range")


