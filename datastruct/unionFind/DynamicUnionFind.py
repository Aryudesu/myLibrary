class RollbackUnionFind:
    """
    ロールバック可能な Union-Find

    特徴:
    - 経路圧縮なし（ロールバックと相性のため）
    - union-by-size
    - snapshot() / rollback(snap) で任意の時点に戻せる
    """
    __slots__ = ("parent", "size", "history", "components")

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        # (child, old_parent, old_size_of_root)
        self.history: list[tuple[int, int, int]] = [] 
        self.components = n

    def leader(self, x: int) -> int:
        """親をたどるだけの leader（経路圧縮なし）"""
        while self.parent[x] != x:
            x = self.parent[x]
        return x

    def same(self, x: int, y: int) -> bool:
        return self.leader(x) == self.leader(y)

    def size_of(self, x: int) -> int:
        return self.size[self.leader(x)]

    def merge(self, x: int, y: int) -> bool:
        """
        x と y の属する集合を union する。
        すでに同じ集合なら False を返し、履歴にはダミーを積む。
        """
        x = self.leader(x)
        y = self.leader(y)
        if x == y:
            # ダミー（rollback のループを簡単にするため）
            self.history.append((-1, -1, -1))
            return False

        # union-by-size: size の大きい方を親にする
        if self.size[x] < self.size[y]:
            x, y = y, x

        # y を x にぶら下げる
        self.history.append((y, self.parent[y], self.size[x]))
        self.parent[y] = x
        self.size[x] += self.size[y]
        self.components -= 1
        return True

    def snapshot(self) -> int:
        """現在の history の長さをスナップショットとして返す"""
        return len(self.history)

    def rollback(self, snapshot: int) -> None:
        """
        snapshot() の返り値まで巻き戻す。
        それ以降の merge はすべて取り消される。
        """
        while len(self.history) > snapshot:
            y, old_parent, old_size = self.history.pop()
            if y == -1:
                # ダミー履歴（union 失敗時）
                continue
            x = self.parent[y]
            self.parent[y] = old_parent
            self.size[x] = old_size
            self.components += 1