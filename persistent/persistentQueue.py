class Node:
    __slots__ = ("value", "prev", "num")
    def __init__(self, val: int | None = None, prev: "Node | None" = None, num: int = 0):
        self.value = val
        self.prev = prev
        self.num = num

class PersistentDequeue:
    """dequeueを永続化…したかったもの"""
    def __init__(self):
        self.pages = dict()
        self.root = Node()
        self.front = self.root
        self.back = self.root

    def _push(self, top:Node, val: int)->Node:
        return Node(val, top, top.num + 1)
    
    def _pop(self, top:Node)->Node:
        if top is self.root:
            return top
        return top.prev
    
    def _top(self, top:Node)->int|None:
        if top is self.root:
            return None
        return top.value

    def append(self, val: int):
        """新規データを右側に追加します"""
        self.front = self._push(self.front, val)

    def appendleft(self, val: int):
        """新規データを左側に追加します"""
        self.back = self._push(self.back, val)

    def pop(self):
        """右端を削除します"""
        self.front = self._pop(self.front)

    def popleft(self):
        """左端を削除します"""
        self.back = self._pop(self.back)

    def bookmark(self, num: int):
        """bookmarkを登録します"""
        self.pages[num] = (self.front, self.back)

    def rollback(self, num: int):
        """bookmarkした情報を復元します"""
        self.front, self.back = self.pages.get(num, (self.root, self.root))

    def isRoot(self)-> bool:
        """現在のデータが空データかを判定します"""
        return self.front is self.root and self.back is self.root

    def getArray(self)-> list[int]:
        """現在の配列を取得します"""
        result = []
        pointer = self.back
        while pointer is not self.root:
            result.append(pointer.value)
            pointer = pointer.prev
        result.reverse()
        rev_result = []
        pointer = self.front
        while pointer is not self.root:
            rev_result.append(pointer.value)
            pointer = pointer.prev
        result.extend(reversed(rev_result))
        return result

    def __len__(self):
        return self.front.num + self.back.num


N = 100
pq = PersistentQueue()
for i in range(N):
    pq.enqueue(i)
    pq.enqueue_front(-i)
print(pq.getArray())
