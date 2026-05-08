class LeftistHeap:
    class Node:
        __slots__ = ("val", "left", "right", "dist")

        def __init__(self, val):
            self.val = val
            self.left = None
            self.right = None
            self.dist = 1

    def __init__(self):
        self.root = None
        self.size = 0

    @staticmethod
    def _dist(node):
        return node.dist if node else 0

    @classmethod
    def _meld(cls, a, b):
        """2つのヒープをマージ"""
        if a is None:
            return b
        if b is None:
            return a

        # min-heap
        if a.val > b.val:
            a, b = b, a

        # 右にmerge
        a.right = cls._meld(a.right, b)

        # leftist condition
        if cls._dist(a.left) < cls._dist(a.right):
            a.left, a.right = a.right, a.left

        a.dist = cls._dist(a.right) + 1
        return a

    def meld(self, other):
        """別ヒープとマージ"""
        self.root = self._meld(self.root, other.root)
        self.size += other.size

    def push(self, x):
        """値追加"""
        node = self.Node(x)
        self.root = self._meld(self.root, node)
        self.size += 1

    def top(self):
        """最小値取得"""
        if self.root is None:
            raise IndexError("heap is empty")
        return self.root.val

    def pop(self):
        """最小値を取り出す"""
        if self.root is None:
            raise IndexError("heap is empty")

        ret = self.root.val
        self.root = self._meld(self.root.left, self.root.right)
        self.size -= 1
        return ret

    def __len__(self):
        return self.size

    def empty(self):
        return self.root is None
    

h1 = LeftistHeap()
h1.push(5)
h1.push(2)

h2 = LeftistHeap()
h2.push(3)
h2.push(1)

h1.meld(h2)

while not h1.empty():
    print(h1.pop())
