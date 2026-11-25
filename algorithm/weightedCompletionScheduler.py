from fractions import Fraction


class WeightedCompletionScheduler:
    """単一機械で重み付き完了時刻の総和を最小化する (Smith's rule).

    time > 0, weight >= 0 の整数を扱う。タスク番号は登録順の0-index。
    """

    def __init__(self):
        self.tasks = []

    def add(self, time: int, weight: int) -> int:
        if time <= 0 or weight < 0:
            raise ValueError("time must be positive and weight nonnegative")
        self.tasks.append((time, weight))
        return len(self.tasks) - 1

    def getOrder(self) -> list[int]:
        """最適順序。同率なら登録順。O(N log N)。"""
        return sorted(range(len(self.tasks)),
                      key=lambda i: Fraction(self.tasks[i][1], self.tasks[i][0]),
                      reverse=True)

    def getCompletionTimes(self) -> list[int]:
        """登録順のタスク番号で参照できる完了時刻。"""
        times = [0] * len(self.tasks)
        now = 0
        for i in self.getOrder():
            now += self.tasks[i][0]
            times[i] = now
        return times

    def getMinCost(self) -> int:
        """最小の重み付き完了時刻総和。O(N log N)。"""
        return sum(c * w for c, (_, w) in
                   zip(self.getCompletionTimes(), self.tasks))
