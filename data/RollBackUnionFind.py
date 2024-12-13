class StackData:
    def __init__(self, A=[]):
        self.pointer = -1
        self.data = []
        for a in A:
            self.data.append(a)
            self.pointer += 1

    def push(self, a):
        """末尾にデータを追加します"""
        if self.pointer + 1 < len(self.data):
            self.data[self.pointer + 1] = a
            self.pointer += 1
        else:
            self.data.append(a)
            self.pointer += 1

    def pop(self):
        """末尾を1つ取り出します"""
        res = self.data[self.pointer]
        self.pointer -= 1
        return res

    def getLast(self):
        """末尾の要素を取得します"""
        return self.data[self.pointer]

    def size(self):
        """サイズを取得します"""
        return self.pointer + 1

    def getIndex(self, index):
        assert index <= self.pointer
        return self.data[index]

class RollBackUnionFind:
    data = []
    history = StackData()
    inner_snap = None

    def __init__(self, size: int = 0):
        self.inner_snap = 0
        self.data = [-1] * size

    def merge(self, x: int, y: int)-> bool:
        """集合の結合"""
        x_ = self.find(x)
        y_ = self.find(y)
        self.history.push([x_, self.data[x_]])
        self.history.push([y_, self.data[y_]])
        if x_ == y_:
            return False
        if self.data[x_] > self.data[y_]:
            x_, y_ = y_, x_
        self.data[x_] += self.data[y_]
        self.data[y_] = x_
        return True

    def leader(self, k: int)-> int:
        """代表元取得"""
        if self.data[k] < 0:
            return k
        return self.find(self.data[k])

    def same(self, x: int, y: int)-> bool:
        """同じ連結成分か"""
        return self.find(x) == self.find(y)

    def size(self, k: int) -> int:
        """サイズ取得"""
        return -self.data[self.find(k)]

    def undo(self):
        """直前の操作取り消し"""
        self.data[self.history.getLast()[0]] = self.history.getLast()[1]
        self.history.pop()
        self.data[self.history.getLast()[0]] = self.history.getLast()[1]
        self.history.pop()

    def snapshot(self):
        """状態保存"""
        self.inner_snap = self.history.size() // 2

    def get_state(self):
        """uniteが呼ばれた回数"""
        return self.history.size() // 2

    def rollback(self, state: int = -1):
        """ロールバック（state==-1のときsnapshot()で保存した所まで）"""
        state_ = state
        if state_ == -1:
            state_ = self.inner_snap
        state_ *= 2
        assert state_ <= self.history.size()
        while state_ < self.history.size():
            self.undo()
