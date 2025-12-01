from sortedcontainers import SortedSet


class IntervalManager:
    def __init__(self):
        self.intervals = SortedSet()

    def add(self, L, R):
        """ 区間 [L, R] を追加し、必要に応じて統合 """
        merged = (L, R)
        
        idx = self.intervals.bisect_left(merged)
        if idx > 0 and self.intervals[idx - 1][1] + 1 >= L:
            idx -= 1

        start_idx = idx
        while idx < len(self.intervals) and self.intervals[idx][0] <= R + 1:
            merged = (min(merged[0], self.intervals[idx][0]), max(merged[1], self.intervals[idx][1]))
            idx += 1

        for _ in range(idx - start_idx):
            self.intervals.pop(start_idx)
        self.intervals.add(merged)

    def find_interval(self, num):
        """ num を含む区間を返す。なければ None """
        idx = self.intervals.bisect_left((num, num))
        if idx < len(self.intervals) and self.intervals[idx][0] <= num <= self.intervals[idx][1]:
            return self.intervals[idx]
        if idx > 0 and self.intervals[idx - 1][0] <= num <= self.intervals[idx - 1][1]:
            return self.intervals[idx - 1]
        return None

    def contains(self, num):
        """ num を含む区間があれば True, なければ False """
        return self.find_interval(num) is not None

    def overlaps(self, L, R):
        """ 区間 [L, R] と重なる部分があるか """
        idx = self.intervals.bisect_left((L, L))
        if idx < len(self.intervals) and self.intervals[idx][0] <= R:
            return True
        if idx > 0 and self.intervals[idx - 1][1] >= L:
            return True
        return False

    def __repr__(self):
        return str(list(self.intervals))

