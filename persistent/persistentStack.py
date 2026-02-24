class Node:
    __slots__ = ("value", "prev", "num")
    def __init__(self, val: int | None = None, prev: "Node | None" = None, num: int = 0):
        self.value = val
        self.prev = prev
        self.num = num

class PersistentStack:
    """保存・ロード機能のある永続スタック"""
    def __init__(self):
        self.pages = dict()
        self.now = Node()
        self.root = self.now

    def push(self, val: int):
        """新規にデータを追加します"""
        self.now = Node(val, self.now, self.now.num + 1)
    
    def pop(self):
        """末尾のスタックを削除します"""
        if self.now is not self.root and self.now.prev is not None:
            self.now = self.now.prev

    def bookmark(self, num: int):
        """bookmarkを登録します"""
        self.pages[num] = self.now

    def rollback(self, num: int):
        """bookmarkに戻ります"""
        assert num in self.pages
        self.now = self.pages.get(num, self.root)

    def top(self)-> int:
        """最後に入力したデータを取得します"""
        return self.now.value

    def isRoot(self)-> bool:
        """現在のデータが空データかを判定します"""
        return self.now is self.root

    def getArray(self)-> list[int]:
        """現在の配列を取得します"""
        result = []
        tmp = self.now
        while not tmp.prev is None:
            result.append(tmp.value)
            tmp = tmp.prev
        result.reverse()
        return result

    def __len__(self):
        return self.now.num

# === ABC273E
nb = PersistentStack()
Q = int(input())
result = []
for _ in range(Q):
    query = input().split()
    if query[0] == "ADD":
        nb.push(int(query[1]))
    elif query[0] == "DELETE":
        nb.pop()
    elif query[0] == "SAVE":
        nb.bookmark(int(query[1]))
    elif query[0] == "LOAD":
        nb.rollback(int(query[1]))
    result.append(-1 if nb.isRoot() else nb.top())
print(*result)
