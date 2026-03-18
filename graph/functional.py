class FunctionalGraph:
    """Functional Graph の始点からの遷移解析"""

    def __init__(self, to: list[int], start: int):
        self.to = to
        self.start = start
        self.order = []
        self.pos = {}
        self.loop_start = -1
        self.loop = []
        self._build()

    def _build(self) -> None:
        now = self.start
        while now not in self.pos:
            self.pos[now] = len(self.order)
            self.order.append(now)
            now = self.to[now]

        self.loop_start = self.pos[now]
        self.loop = self.order[self.loop_start:]

    def kth(self, k: int) -> int:
        """start から k 回遷移した先を返す"""
        if k < len(self.order):
            return self.order[k]
        return self.loop[(k - self.loop_start) % len(self.loop)]

    def is_in_loop(self, v: int) -> bool:
        """v が start から到達するループ部分に含まれるか"""
        return v in self.pos and self.pos[v] >= self.loop_start

