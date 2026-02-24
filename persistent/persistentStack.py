class Node:
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
        self.now = Node(val, self.now, self.now.num + 1)
    
    def pop(self):
        if (not self.now is self.root) and (not self.now.prev is None):
            self.now = self.now.prev

    def bookmark(self, num: int):
        self.pages[num] = self.now

    def rollback(self, num: int):
        self.now = self.pages.get(num, self.root)

    def getLast(self)-> int:
        return self.now.value

    def isRoot(self)-> bool:
        return self.now is self.root

    def getArray(self)-> list[int]:
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
    result.append(-1 if nb.isRoot() else nb.getLast())
print(*result)
