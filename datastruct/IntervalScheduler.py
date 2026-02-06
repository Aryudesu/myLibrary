class IntervalScheduler:
    """区間スケジューリング問題（区間数最大問題）"""
    def __init__(self):
        self.schedule = []

    def add(self, start: int, end: int):
        """[start, end)の区間を追加します"""
        self.schedule.append((end, start))

    def solve(self):
        """選ぶことが可能な区間の最大数を返却します"""
        self.schedule.sort()
        now = 0
        count = 0
        for end, start in self.schedule:
            if now > start:
                continue
            now = end
            count += 1
        return count

# 競技プログラミングの鉄則 A39
N = int(input())
isr = IntervalScheduler()
for n in range(N):
    l, r = map(int, input().split())
    isr.add(l, r)
print(isr.solve())
