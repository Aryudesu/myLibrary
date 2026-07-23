class ArrayLinkedList:
    """0..N の整数をノードとして使う配列版連結リスト"""
    def __init__(self, max_val: int):
        self.prev = [-1] * (max_val + 1)
        self.nxt = [-1] * (max_val + 1)
        self.head = -1

    def init_single(self, v: int):
        """v だけが入ったリストに初期化"""
        self.head = v
        self.prev[v] = -1
        self.nxt[v] = -1

    def insert_after(self, x: int, v: int):
        """x の直後に v を挿入"""
        nx = self.nxt[x]
        self.nxt[x] = v
        self.prev[v] = x
        self.nxt[v] = nx
        if nx != -1:
            self.prev[nx] = v

    def delete(self, v: int):
        """v をリストから削除"""
        p = self.prev[v]
        n = self.nxt[v]
        if p != -1:
            self.nxt[p] = n
        else:
            self.head = n
        if n != -1:
            self.prev[n] = p
        self.prev[v] = -1
        self.nxt[v] = -1

    def to_list(self):
        res = []
        cur = self.head
        while cur != -1:
            res.append(cur)
            cur = self.nxt[cur]
        return res
